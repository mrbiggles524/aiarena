"""
Agent model and related schemas
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AgentStatus(str, enum.Enum):
    """Agent status"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    UNDER_REVIEW = "under_review"


class AgentProvider(str, enum.Enum):
    """AI provider for agent"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROK = "grok"
    CUSTOM = "custom"


class Agent(Base):
    """AI Agent model"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Agent configuration (JSON)
    config = Column(JSON, nullable=False)  # {"model": "gpt-4", "temperature": 0.7, "tools": [...]}
    code = Column(Text, nullable=True)  # Agent code/script (if custom)
    
    # Provider
    provider = Column(SQLEnum(AgentProvider), default=AgentProvider.OPENAI)
    provider_model = Column(String, nullable=False)  # e.g., "gpt-4-turbo", "claude-3-5-sonnet"
    
    # Capabilities (JSON array)
    capabilities = Column(Text, nullable=True)  # JSON: ["web_scraping", "email", "data_analysis"]
    
    # Status
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT, index=True)
    
    # Relationships
    builder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    builder = relationship("User", back_populates="agents")
    
    # Stats
    total_competitions = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    total_earnings = Column(Float, default=0.0)
    reputation_score = Column(Float, default=0.0)
    average_score = Column(Float, default=0.0)
    
    # Evolution
    version = Column(Integer, default=1)
    parent_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    parent_agent = relationship("Agent", remote_side=[id])
    evolution_history = Column(Text, nullable=True)  # JSON: [{"version": 1, "improvements": [...]}]
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    tags = Column(String, nullable=True)
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    participations = relationship("ArenaParticipation", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent {self.name} (v{self.version})>"

