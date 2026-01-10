"""
Bounty management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models.bounty import Bounty, BountyStatus, BountyType
from app.models.user import User, UserRole
from app.api.auth import get_current_user
from app.config import settings

router = APIRouter()


class BountyCreate(BaseModel):
    title: str
    description: str
    bounty_type: BountyType
    budget: float
    success_criteria: dict  # JSON object
    requirements: dict = None  # JSON object
    expires_at: datetime = None
    tags: str = None
    payment_method: str = "fiat"  # "fiat" or "crypto"
    crypto_type: str = None  # "BTC", "ETH", "USDT", etc.
    crypto_wallet_address: str = None  # Wallet address for receiving crypto payments


class BountyResponse(BaseModel):
    id: int
    title: str
    description: str
    bounty_type: str
    budget: float
    platform_fee: float
    agent_reward: float
    success_criteria: str
    status: str
    poster_id: int
    created_at: datetime
    payment_method: str = "fiat"
    crypto_type: str = None
    crypto_wallet_address: str = None
    crypto_amount: float = None
    
    class Config:
        from_attributes = True


@router.post("/", response_model=BountyResponse, status_code=201)
async def create_bounty(
    bounty_data: BountyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new bounty"""
    # Allow all authenticated users to create bounties (role check removed)
    # DEBUG: Log that we're creating a bounty without role check
    print(f"[DEBUG] Creating bounty for user {current_user.id} ({current_user.username}) - no role check")
    
    # Calculate fees
    platform_fee = bounty_data.budget * (settings.PLATFORM_FEE_PERCENTAGE / 100)
    agent_reward = bounty_data.budget * (settings.AGENT_REWARD_PERCENTAGE / 100)
    
    # Handle crypto payments
    crypto_amount = None
    if bounty_data.payment_method == "crypto" and bounty_data.crypto_type:
        # Convert USD to crypto (using approximate rates - in production, use real-time API)
        crypto_rates = {
            "BTC": 45000.0,  # Approximate BTC price in USD
            "ETH": 2500.0,   # Approximate ETH price in USD
            "USDT": 1.0,     # Stablecoin
            "USDC": 1.0,     # Stablecoin
            "SOL": 100.0,    # Approximate SOL price in USD
            "MATIC": 0.8,    # Approximate MATIC price in USD
        }
        rate = crypto_rates.get(bounty_data.crypto_type.upper(), 1.0)
        if rate > 0:
            crypto_amount = bounty_data.budget / rate
    
    # Create bounty
    import json
    bounty = Bounty(
        title=bounty_data.title,
        description=bounty_data.description,
        bounty_type=bounty_data.bounty_type,
        budget=bounty_data.budget,
        platform_fee=platform_fee,
        agent_reward=agent_reward,
        success_criteria=json.dumps(bounty_data.success_criteria),
        requirements=json.dumps(bounty_data.requirements) if bounty_data.requirements else None,
        poster_id=current_user.id,
        status=BountyStatus.DRAFT,
        expires_at=bounty_data.expires_at,
        tags=bounty_data.tags,
        payment_method=bounty_data.payment_method or "fiat",
        crypto_type=bounty_data.crypto_type,
        crypto_wallet_address=bounty_data.crypto_wallet_address,
        crypto_amount=crypto_amount
    )
    
    db.add(bounty)
    db.commit()
    db.refresh(bounty)
    
    return bounty


@router.get("/", response_model=List[BountyResponse])
async def list_bounties(
    status: Optional[BountyStatus] = Query(None),
    bounty_type: Optional[BountyType] = Query(None),
    min_budget: Optional[float] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all bounties with filters"""
    query = db.query(Bounty)
    
    if status:
        query = query.filter(Bounty.status == status)
    if bounty_type:
        query = query.filter(Bounty.bounty_type == bounty_type)
    if min_budget:
        query = query.filter(Bounty.budget >= min_budget)
    
    bounties = query.order_by(desc(Bounty.created_at)).offset(offset).limit(limit).all()
    return bounties


@router.get("/{bounty_id}", response_model=BountyResponse)
async def get_bounty(bounty_id: int, db: Session = Depends(get_db)):
    """Get bounty by ID"""
    bounty = db.query(Bounty).filter(Bounty.id == bounty_id).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    # Increment view count
    bounty.view_count += 1
    db.commit()
    
    return bounty


@router.put("/{bounty_id}/publish", response_model=BountyResponse)
async def publish_bounty(
    bounty_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish a draft bounty (make it open for agents)"""
    bounty = db.query(Bounty).filter(Bounty.id == bounty_id).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    if bounty.poster_id != current_user.id and not current_user.has_role(UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if bounty.status != BountyStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Bounty is not in draft status")
    
    bounty.status = BountyStatus.OPEN
    db.commit()
    db.refresh(bounty)
    
    return bounty

