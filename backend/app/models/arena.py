"""
Arena model for competitions
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ArenaStatus(str, enum.Enum):
    """Arena competition status"""
    SCHEDULED = "scheduled"
    REGISTRATION_OPEN = "registration_open"
    IN_PROGRESS = "in_progress"
    JUDGING = "judging"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Arena(Base):
    """Arena competition model"""
    __tablename__ = "arenas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Status
    status = Column(SQLEnum(ArenaStatus), default=ArenaStatus.REGISTRATION_OPEN, index=True)
    
    # Bounty (one-to-one relationship)
    bounty_id = Column(Integer, ForeignKey("bounties.id"), nullable=False, unique=True)
    bounty = relationship("Bounty", uselist=False, foreign_keys=[bounty_id])
    
    # Competition settings
    max_participants = Column(Integer, default=10)
    min_participants = Column(Integer, default=2)
    simulation_duration_seconds = Column(Integer, default=300)  # 5 minutes default
    
    # Participants
    participants = relationship("ArenaParticipation", back_populates="arena", cascade="all, delete-orphan")
    
    # Results
    winner_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    winner = relationship("Agent", foreign_keys=[winner_id])
    
    results = Column(JSON, nullable=True)  # Full results JSON
    judge_feedback = Column(Text, nullable=True)  # AI judge's detailed feedback
    
    # Spectator settings
    is_public = Column(Boolean, default=True)
    spectator_count = Column(Integer, default=0)
    max_spectators = Column(Integer, default=1000)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    scheduled_start = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Arena {self.name} ({self.status.value})>"


class ArenaParticipation(Base):
    """Agent participation in an arena"""
    __tablename__ = "arena_participations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    arena_id = Column(Integer, ForeignKey("arenas.id"), nullable=False)
    arena = relationship("Arena", back_populates="participants")
    
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    agent = relationship("Agent", back_populates="participations")
    
    agent_builder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_builder = relationship("User", back_populates="arena_participations")
    
    # Performance
    score = Column(Float, nullable=True)  # Final score from judge
    rank = Column(Integer, nullable=True)  # Final rank (1 = winner)
    
    # Execution data
    execution_log = Column(Text, nullable=True)  # JSON: agent's actions during competition
    output_data = Column(JSON, nullable=True)  # Agent's output/results
    error_log = Column(Text, nullable=True)  # Any errors encountered
    
    # Resources used
    execution_time_seconds = Column(Float, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    api_calls_made = Column(Integer, nullable=True)
    
    # Reward
    reward_amount = Column(Float, default=0.0)
    reward_paid = Column(Boolean, default=False)
    
    # Timestamps
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<ArenaParticipation Agent {self.agent_id} in Arena {self.arena_id}>"

