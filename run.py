"""
Quick start script for AI Agent Bounty Arena
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def setup_database():
    """Initialize database"""
    print("📦 Setting up database...")
    # Database will be created automatically on first run
    print("✅ Database ready")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 Creating .env file...")
        with open(env_path, "w") as f:
            f.write("""# AI Agent Bounty Arena - Environment Variables
DATABASE_URL=sqlite:///./aiarena.db
SECRET_KEY=change-this-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Provider API Keys (add your keys)
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
GOOGLE_API_KEY=your-google-key-here

# Platform Settings
PLATFORM_FEE_PERCENTAGE=15
AGENT_REWARD_PERCENTAGE=80
RUNNER_UP_REWARD_PERCENTAGE=5

# Sandbox Settings
SANDBOX_TIMEOUT_SECONDS=300
MAX_AGENT_MEMORY_MB=512
MAX_AGENT_CPU_PERCENT=50

# Judge Settings
JUDGE_MODEL=claude-3-5-sonnet-20241022
JUDGE_TEMPERATURE=0.3

# Frontend
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
""")
        print("✅ .env file created. Please update with your API keys!")
    else:
        print("✅ .env file exists")

def main():
    """Main startup function"""
    print("🚀 Starting AI Agent Bounty Arena...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return
    
    os.chdir(backend_dir)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup
    create_env_file()
    setup_database()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your API keys")
    print("2. Start the server: python run.py")
    print("3. Open http://localhost:8000/docs for API docs")
    print("4. Open frontend/index.html in your browser")
    print("\n🎮 Ready to start competitions!")

if __name__ == "__main__":
    main()

