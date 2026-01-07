"""
Arena competition endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from pydantic import BaseModel
from datetime import datetime
import json

from app.database import get_db
from app.models.arena import Arena, ArenaStatus, ArenaParticipation
from app.models.bounty import Bounty, BountyStatus
from app.models.agent import Agent, AgentStatus
from app.models.user import User, UserRole
from app.api.auth import get_current_user
from app.services.arena_runner import ArenaRunner
from app.services.judge import JudgeService

router = APIRouter()


class ArenaCreate(BaseModel):
    bounty_id: int
    max_participants: int = 10
    min_participants: int = 2
    simulation_duration_seconds: int = 300


class ArenaResponse(BaseModel):
    id: int
    name: str
    status: str
    bounty_id: int
    max_participants: int
    current_participants: int
    created_at: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ArenaResponse, status_code=201)
async def create_arena(
    arena_data: ArenaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new arena competition for a bounty"""
    # Get bounty
    bounty = db.query(Bounty).filter(Bounty.id == arena_data.bounty_id).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    if bounty.poster_id != current_user.id and not current_user.has_role(UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if bounty.status != BountyStatus.OPEN:
        raise HTTPException(status_code=400, detail="Bounty must be open")
    
    # Check if arena already exists
    existing_arena = db.query(Arena).filter(Arena.bounty_id == arena_data.bounty_id).first()
    if existing_arena:
        raise HTTPException(status_code=400, detail="Arena already exists for this bounty")
    
    # Create arena
    arena = Arena(
        name=f"Arena: {bounty.title}",
        description=f"Competition for bounty: {bounty.description}",
        bounty_id=bounty.id,
        max_participants=arena_data.max_participants,
        min_participants=arena_data.min_participants,
        simulation_duration_seconds=arena_data.simulation_duration_seconds,
        status=ArenaStatus.REGISTRATION_OPEN
    )
    
    db.add(arena)
    bounty.status = BountyStatus.IN_PROGRESS
    db.commit()
    db.refresh(arena)
    
    return arena


@router.post("/{arena_id}/register")
async def register_agent(
    arena_id: int,
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register an agent to participate in an arena"""
    arena = db.query(Arena).filter(Arena.id == arena_id).first()
    if not arena:
        raise HTTPException(status_code=404, detail="Arena not found")
    
    if arena.status != ArenaStatus.REGISTRATION_OPEN:
        raise HTTPException(status_code=400, detail="Arena registration is closed")
    
    # Get agent
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent.builder_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your agent")
    
    if agent.status != AgentStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Agent must be active")
    
    # Check if already registered
    existing = db.query(ArenaParticipation).filter(
        ArenaParticipation.arena_id == arena_id,
        ArenaParticipation.agent_id == agent_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Agent already registered")
    
    # Check participant limit
    current_count = db.query(ArenaParticipation).filter(
        ArenaParticipation.arena_id == arena_id
    ).count()
    if current_count >= arena.max_participants:
        raise HTTPException(status_code=400, detail="Arena is full")
    
    # Register agent
    participation = ArenaParticipation(
        arena_id=arena_id,
        agent_id=agent_id,
        agent_builder_id=current_user.id
    )
    
    db.add(participation)
    db.commit()
    
    return {"message": "Agent registered successfully", "participation_id": participation.id}


@router.post("/{arena_id}/start")
async def start_arena(
    arena_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start an arena competition"""
    arena = db.query(Arena).filter(Arena.id == arena_id).first()
    if not arena:
        raise HTTPException(status_code=404, detail="Arena not found")
    
    # Check authorization
    bounty = db.query(Bounty).filter(Bounty.id == arena.bounty_id).first()
    if bounty.poster_id != current_user.id and not current_user.has_role(UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if arena.status != ArenaStatus.REGISTRATION_OPEN:
        raise HTTPException(status_code=400, detail="Arena cannot be started")
    
    # Check minimum participants
    participant_count = db.query(ArenaParticipation).filter(
        ArenaParticipation.arena_id == arena_id
    ).count()
    if participant_count < arena.min_participants:
        raise HTTPException(status_code=400, detail=f"Need at least {arena.min_participants} participants")
    
    # Start arena
    arena.status = ArenaStatus.IN_PROGRESS
    arena.started_at = datetime.utcnow()
    db.commit()
    
    # Run arena competition (async)
    from app.services.arena_runner import ArenaRunner
    arena_runner = ArenaRunner()
    # This would typically be run in a background task
    # For now, we'll return immediately and handle async execution separately
    
    return {"message": "Arena started", "arena_id": arena_id}


@router.get("/{arena_id}", response_model=ArenaResponse)
async def get_arena(arena_id: int, db: Session = Depends(get_db)):
    """Get arena details"""
    arena = db.query(Arena).filter(Arena.id == arena_id).first()
    if not arena:
        raise HTTPException(status_code=404, detail="Arena not found")
    
    participant_count = db.query(ArenaParticipation).filter(
        ArenaParticipation.arena_id == arena_id
    ).count()
    
    return {
        "id": arena.id,
        "name": arena.name,
        "status": arena.status.value,
        "bounty_id": arena.bounty_id,
        "max_participants": arena.max_participants,
        "current_participants": participant_count,
        "created_at": arena.created_at.isoformat()
    }


@router.get("/", response_model=List[ArenaResponse])
async def list_arenas(
    status: ArenaStatus = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all arenas"""
    query = db.query(Arena)
    if status:
        query = query.filter(Arena.status == status)
    
    arenas = query.order_by(desc(Arena.created_at)).offset(offset).limit(limit).all()
    
    result = []
    for arena in arenas:
        participant_count = db.query(ArenaParticipation).filter(
            ArenaParticipation.arena_id == arena.id
        ).count()
        result.append({
            "id": arena.id,
            "name": arena.name,
            "status": arena.status.value,
            "bounty_id": arena.bounty_id,
            "max_participants": arena.max_participants,
            "current_participants": participant_count,
            "created_at": arena.created_at.isoformat()
        })
    
    return result


@router.websocket("/{arena_id}/watch")
async def watch_arena(websocket: WebSocket, arena_id: int, db: Session = Depends(get_db)):
    """WebSocket endpoint for watching live arena competitions"""
    await websocket.accept()
    
    arena = db.query(Arena).filter(Arena.id == arena_id).first()
    if not arena:
        await websocket.close(code=1008, reason="Arena not found")
        return
    
    try:
        while True:
            # Send arena updates
            participant_count = db.query(ArenaParticipation).filter(
                ArenaParticipation.arena_id == arena_id
            ).count()
            
            await websocket.send_json({
                "arena_id": arena_id,
                "status": arena.status.value,
                "participants": participant_count,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Wait for next update (simplified - in production, use proper event system)
            import asyncio
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        pass

