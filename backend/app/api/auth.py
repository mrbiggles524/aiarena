"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User, UserRole
from app.config import settings

router = APIRouter()
security = HTTPBearer()
# Use pbkdf2_sha256 (more compatible than bcrypt on some systems)
# bcrypt has compatibility issues with newer Python versions
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str | None = None
    roles: list[str] = ["spectator"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str = None
    roles: str
    balance: float = 0.0
    reputation_score: float = 0.0
    is_premium: bool = False
    
    class Config:
        from_attributes = True


# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials.strip()  # Remove any leading/trailing whitespace
        if not token:
            raise credentials_exception
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)  # Convert string back to int
    except (JWTError, ValueError, TypeError) as e:
        # Log the error for debugging
        from loguru import logger
        logger.error(f"Token validation error: {type(e).__name__}: {str(e)}")
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user


# Routes
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        # Convert role strings to UserRole enums if needed, then join
        role_values = []
        for role_str in user_data.roles:
            try:
                role_enum = UserRole(role_str)
                role_values.append(role_enum.value)
            except ValueError:
                # Invalid role, skip or use default
                role_values.append(UserRole.SPECTATOR.value)
        roles_str = ",".join(role_values) if role_values else UserRole.SPECTATOR.value
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            roles=roles_str
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},  # JWT subject must be a string
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "roles": user.roles
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        from loguru import logger
        error_msg = str(e)
        traceback.print_exc()
        logger.error(f"Registration error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {error_msg}")


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    # Create token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},  # JWT subject must be a string
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "roles": user.roles
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user information"""
    try:
        # Refresh user from database to ensure all fields are loaded
        db.refresh(current_user)
        
        # Ensure all required fields have defaults
        user_data = {
            "id": current_user.id,
            "email": current_user.email or "",
            "username": current_user.username or "",
            "full_name": current_user.full_name,
            "roles": current_user.roles or "spectator",
            "balance": float(current_user.balance) if current_user.balance is not None else 0.0,
            "reputation_score": float(current_user.reputation_score) if current_user.reputation_score is not None else 0.0,
            "is_premium": bool(current_user.is_premium) if current_user.is_premium is not None else False
        }
        
        return UserResponse(**user_data)
    except Exception as e:
        from loguru import logger
        logger.error(f"Error serializing user {current_user.id if current_user else 'unknown'}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving user info: {str(e)}")

