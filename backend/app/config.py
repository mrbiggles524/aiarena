"""
Configuration settings for AI Agent Bounty Arena
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    # Railway automatically provides DATABASE_URL for PostgreSQL
    # Priority: 1. DATABASE_URL env var, 2. POSTGRES_URL (Railway), 3. SQLite (local only)
    _db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or os.getenv("PGDATABASE")
    
    # On Railway, we MUST use PostgreSQL - fail if SQLite is detected
    if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY"):
        if not _db_url or _db_url.startswith("sqlite"):
            # Try to find PostgreSQL URL from Railway's service variables
            # Railway sometimes provides it as POSTGRES_URL or in service variables
            import warnings
            warnings.warn(
                "⚠️  WARNING: No PostgreSQL DATABASE_URL found on Railway! "
                "Data will be lost. Check Railway Variables tab and ensure PostgreSQL service is linked."
            )
            # Still allow SQLite for now, but log warning
            _db_url = _db_url or "sqlite:///./aiarena.db"
    
    DATABASE_URL: str = _db_url or "sqlite:///./aiarena.db"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # AI Provider API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GROK_API_KEY: str = os.getenv("GROK_API_KEY", "")
    
    # Platform Economics
    PLATFORM_FEE_PERCENTAGE: float = float(os.getenv("PLATFORM_FEE_PERCENTAGE", "15"))
    AGENT_REWARD_PERCENTAGE: float = float(os.getenv("AGENT_REWARD_PERCENTAGE", "80"))
    RUNNER_UP_REWARD_PERCENTAGE: float = float(os.getenv("RUNNER_UP_REWARD_PERCENTAGE", "5"))
    
    # Payment Processing
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    
    # Sandbox Settings
    SANDBOX_TIMEOUT_SECONDS: int = int(os.getenv("SANDBOX_TIMEOUT_SECONDS", "300"))
    MAX_AGENT_MEMORY_MB: int = int(os.getenv("MAX_AGENT_MEMORY_MB", "512"))
    MAX_AGENT_CPU_PERCENT: int = int(os.getenv("MAX_AGENT_CPU_PERCENT", "50"))
    
    # Judge Settings
    JUDGE_MODEL: str = os.getenv("JUDGE_MODEL", "claude-3-5-sonnet-20241022")
    JUDGE_TEMPERATURE: float = float(os.getenv("JUDGE_TEMPERATURE", "0.3"))
    
    # Frontend
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()

