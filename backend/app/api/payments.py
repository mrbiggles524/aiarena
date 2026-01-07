"""
Payment processing endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter()

# Initialize Stripe (if configured and available)
try:
    import stripe
    if settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
    STRIPE_AVAILABLE = True
except ImportError:
    stripe = None
    STRIPE_AVAILABLE = False


class PaymentIntentCreate(BaseModel):
    amount: float
    currency: str = "usd"
    description: str = None


@router.post("/create-intent")
async def create_payment_intent(
    payment_data: PaymentIntentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe payment intent"""
    if not STRIPE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Stripe package not installed. Run: pip install stripe")
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Payment processing not configured")
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payment_data.amount * 100),  # Convert to cents
            currency=payment_data.currency,
            description=payment_data.description,
            metadata={"user_id": current_user.id}
        )
        
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: dict):
    """Handle Stripe webhook events"""
    # Webhook handling logic here
    # Verify signature, process events, update user balances
    return {"status": "ok"}

