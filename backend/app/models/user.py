"""
User model and related schemas
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """User roles in the platform"""
    BOUNTY_POSTER = "bounty_poster"
    AGENT_BUILDER = "agent_builder"
    SPECTATOR = "spectator"
    ADMIN = "admin"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    
    # Roles (users can have multiple roles)
    roles = Column(String, default=UserRole.SPECTATOR.value)  # Comma-separated roles
    
    # Profile
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Wallet/Balance
    balance = Column(Float, default=0.0)  # Platform credits/balance
    
    # Stats
    total_earnings = Column(Float, default=0.0)
    total_spent = Column(Float, default=0.0)
    reputation_score = Column(Float, default=0.0)
    
    # Subscription
    is_premium = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    bounties = relationship("Bounty", back_populates="poster", foreign_keys="Bounty.poster_id")
    agents = relationship("Agent", back_populates="builder")
    arena_participations = relationship("ArenaParticipation", back_populates="agent_builder")
    
    def has_role(self, role: UserRole) -> bool:
        """Check if user has a specific role"""
        return role.value in self.roles.split(",")
    
    def add_role(self, role: UserRole):
        """Add a role to user"""
        roles_list = self.roles.split(",") if self.roles else []
        if role.value not in roles_list:
            roles_list.append(role.value)
            self.roles = ",".join(roles_list)
    
    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

