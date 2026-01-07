"""
Bounty model and related schemas
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class BountyStatus(str, enum.Enum):
    """Bounty status"""
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class BountyType(str, enum.Enum):
    """Type of bounty task"""
    LEAD_GENERATION = "lead_generation"
    CONTENT_CREATION = "content_creation"
    DATA_ANALYSIS = "data_analysis"
    SEO_OPTIMIZATION = "seo_optimization"
    SOCIAL_MEDIA = "social_media"
    RESEARCH = "research"
    AUTOMATION = "automation"
    OTHER = "other"


class Bounty(Base):
    """Bounty model"""
    __tablename__ = "bounties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Bounty details
    bounty_type = Column(SQLEnum(BountyType), default=BountyType.OTHER)
    budget = Column(Float, nullable=False)  # Total budget in USD
    platform_fee = Column(Float, nullable=False)  # Platform fee (15%)
    agent_reward = Column(Float, nullable=False)  # Winner reward (80%)
    
    # Success criteria (JSON string for flexibility)
    success_criteria = Column(Text, nullable=False)  # JSON: {"metric": "conversion_rate", "target": 20, "unit": "%"}
    
    # Requirements
    requirements = Column(Text, nullable=True)  # JSON: {"min_agent_reputation": 50, "allowed_agents": [...]}
    
    # Status
    status = Column(SQLEnum(BountyStatus), default=BountyStatus.DRAFT, index=True)
    
    # Relationships
    poster_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    poster = relationship("User", back_populates="bounties", foreign_keys=[poster_id])
    
    # Arena (optional - arena references this bounty via bounty_id)
    arena_id = Column(Integer, ForeignKey("arenas.id"), nullable=True)
    # No relationship here - Arena has the relationship to Bounty
    
    # Results
    winning_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    winning_agent = relationship("Agent", foreign_keys=[winning_agent_id])
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    tags = Column(String, nullable=True)  # Comma-separated tags
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Bounty {self.title} (${self.budget})>"

