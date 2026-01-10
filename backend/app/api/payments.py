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


class CryptoPaymentCreate(BaseModel):
    bounty_id: int
    crypto_type: str  # "BTC", "ETH", "USDT", etc.
    transaction_hash: str  # Blockchain transaction hash
    amount: float  # Amount in crypto
    wallet_address: str  # Sender wallet address


@router.post("/crypto/verify")
async def verify_crypto_payment(
    payment_data: CryptoPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify a cryptocurrency payment for a bounty"""
    from app.models.bounty import Bounty
    
    bounty = db.query(Bounty).filter(Bounty.id == payment_data.bounty_id).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    if bounty.poster_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # In production, verify transaction on blockchain
    # For now, we'll just store the payment info
    # You would integrate with blockchain APIs like:
    # - Bitcoin: BlockCypher, Blockchain.info
    # - Ethereum: Etherscan, Infura
    # - Solana: Solscan, Helius
    
    return {
        "status": "pending_verification",
        "message": "Payment submitted. Verification in progress.",
        "transaction_hash": payment_data.transaction_hash,
        "note": "In production, this would verify the transaction on the blockchain"
    }


@router.get("/crypto/rates")
async def get_crypto_rates():
    """Get current cryptocurrency exchange rates"""
    # In production, fetch from CoinGecko, CoinMarketCap, or similar API
    return {
        "BTC": 45000.0,  # Approximate - use real API in production
        "ETH": 2500.0,
        "USDT": 1.0,
        "USDC": 1.0,
        "SOL": 100.0,
        "MATIC": 0.8,
        "note": "These are approximate rates. Use real-time API in production."
    }
