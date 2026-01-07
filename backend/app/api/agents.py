"""
Agent management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.agent import Agent, AgentStatus, AgentProvider
from app.models.user import User, UserRole
from app.api.auth import get_current_user

router = APIRouter()


class AgentCreate(BaseModel):
    name: str
    description: str = None
    config: dict  # Agent configuration JSON
    provider: AgentProvider
    provider_model: str
    capabilities: List[str] = []
    code: str = None  # Custom agent code
    tags: str = None


class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    provider: str
    provider_model: str
    status: str
    builder_id: int
    total_competitions: int
    total_wins: int
    win_rate: float
    reputation_score: float
    created_at: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=AgentResponse, status_code=201)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new AI agent"""
    # Check if user has agent builder role
    if not current_user.has_role(UserRole.AGENT_BUILDER) and not current_user.has_role(UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="You need agent builder role to create agents")
    
    import json
    agent = Agent(
        name=agent_data.name,
        description=agent_data.description,
        config=agent_data.config,
        provider=agent_data.provider,
        provider_model=agent_data.provider_model,
        capabilities=json.dumps(agent_data.capabilities),
        code=agent_data.code,
        builder_id=current_user.id,
        status=AgentStatus.UNDER_REVIEW,
        tags=agent_data.tags
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    status: Optional[AgentStatus] = Query(None),
    provider: Optional[AgentProvider] = Query(None),
    builder_id: Optional[int] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all agents with filters"""
    query = db.query(Agent).filter(Agent.is_public == True)
    
    if status:
        query = query.filter(Agent.status == status)
    if provider:
        query = query.filter(Agent.provider == provider)
    if builder_id:
        query = query.filter(Agent.builder_id == builder_id)
    
    agents = query.order_by(desc(Agent.reputation_score)).offset(offset).limit(limit).all()
    return agents


@router.get("/my-agents", response_model=List[AgentResponse])
async def get_my_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's agents"""
    agents = db.query(Agent).filter(Agent.builder_id == current_user.id).all()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent


@router.post("/{agent_id}/activate")
async def activate_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate an agent (make it available for competitions)"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent.builder_id != current_user.id and not current_user.has_role(UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if agent.status != AgentStatus.UNDER_REVIEW:
        raise HTTPException(status_code=400, detail="Agent must be under review first")
    
    agent.status = AgentStatus.ACTIVE
    db.commit()
    
    return {"message": "Agent activated successfully"}

