"""
AI Agent Bounty Arena - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
import os

from app.database import engine, Base, get_db
from app.api import auth, bounties, agents, arenas, users, payments
from app.config import settings
from sqlalchemy import desc

# Initialize logger
import os
# Create logs directory if it doesn't exist (may fail in read-only filesystems, that's OK)
try:
    os.makedirs("logs", exist_ok=True)
    logger.add("logs/aiarena.log", rotation="10 MB", retention="7 days", level="INFO")
except (OSError, PermissionError):
    # If we can't create logs directory, just log to console (Railway will capture this)
    logger.add(lambda msg: print(msg), level="INFO")

# Security
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting AI Agent Bounty Arena...")
    
    # Create database tables (only if they don't exist - safe for production)
    # This will NOT drop existing tables or data
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
        db_type = "PostgreSQL" if settings.DATABASE_URL.startswith("postgresql") else "SQLite"
        logger.info(f"✅ Database tables verified/created using {db_type} (existing data preserved)")
        
        # Warn if using SQLite on Railway (data won't persist)
        if os.getenv("RAILWAY_ENVIRONMENT") and settings.DATABASE_URL.startswith("sqlite"):
            logger.warning("⚠️  WARNING: Using SQLite on Railway - data will be lost on deployments!")
            logger.warning("⚠️  Add PostgreSQL database in Railway to persist data.")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        # Don't crash - allow app to start even if DB init fails
        # The error will show up in health check
        import traceback
        traceback.print_exc()
    
    # Initialize agent sandbox
    from app.services.sandbox import SandboxManager
    sandbox_manager = SandboxManager()
    await sandbox_manager.initialize()
    app.state.sandbox_manager = sandbox_manager
    logger.info("✅ Agent sandbox initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AI Agent Bounty Arena...")
    if hasattr(app.state, 'sandbox_manager'):
        await app.state.sandbox_manager.cleanup()


# Load frontend HTML BEFORE creating the app
# Use absolute path to avoid any path resolution issues
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
_frontend_dir = os.path.join(_parent_dir, "frontend")
_index_file = os.path.join(_frontend_dir, "index.html")

# Normalize to absolute path
index_path = os.path.abspath(_index_file) if os.path.exists(_index_file) else None
frontend_path = os.path.abspath(_frontend_dir) if os.path.exists(_frontend_dir) else None
html_content = None

if index_path and os.path.exists(index_path):
    print(f"[OK] Found frontend at: {frontend_path}")
    print(f"[OK] Index file: {index_path}")
else:
    # Try alternative paths
    possible_paths = [
        "C:\\AIArena\\frontend\\index.html",
        os.path.join(_current_dir, "..", "frontend", "index.html"),
    ]
    for alt_path in possible_paths:
        abs_alt = os.path.abspath(alt_path)
        if os.path.exists(abs_alt):
            index_path = abs_alt
            frontend_path = os.path.dirname(abs_alt)
            print(f"[OK] Found frontend at alternative path: {frontend_path}")
            break

if index_path and os.path.exists(index_path):
    try:
        # Force reload by reading fresh each time
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"[OK] Frontend HTML loaded successfully ({len(html_content)} characters)")
        print(f"[OK] HTML file path: {index_path}")
        print(f"[OK] File contains Inter font: {'Inter' in html_content}")
        print(f"[OK] File contains new CSS: {'#6366f1' in html_content}")
    except Exception as e:
        print(f"[ERROR] Error reading frontend HTML: {e}")
        html_content = None
else:
    print(f"[WARNING] Frontend not found. Tried paths: {possible_paths}")

# Create FastAPI app
app = FastAPI(
    title="AI Agent Bounty Arena API",
    description="Competitive marketplace for AI agents and business bounties",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
# In production, frontend is served from same origin, so we need to allow the Railway domain
# Get the current host from environment or use FRONTEND_URL
if settings.ENVIRONMENT == "production" or os.getenv("RAILWAY_ENVIRONMENT"):
    # Production: allow the Railway domain and FRONTEND_URL
    cors_origins = [
        settings.FRONTEND_URL,
        "https://web-production-fb8c.up.railway.app",
        "http://localhost:8000",  # For local testing
    ]
    # Remove duplicates and empty strings
    cors_origins = list(set([origin for origin in cors_origins if origin]))
else:
    # Development: use FRONTEND_URL
    cors_origins = settings.FRONTEND_URL.split(",") if "," in settings.FRONTEND_URL else [settings.FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define root route FIRST (before other routes)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Root endpoint - serves frontend"""
    # ALWAYS read fresh from disk - use absolute path
    html_file = os.path.abspath("C:\\AIArena\\frontend\\index.html")
    
    # Verify file exists and read it
    if not os.path.exists(html_file):
        # Try alternative path
        html_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))
    
    if os.path.exists(html_file):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                fresh_html = f.read()
            # Log for debugging
            logger.info(f"Serving HTML from: {html_file}")
            logger.info(f"HTML size: {len(fresh_html)} bytes")
            logger.info(f"Has new CSS: {'#6366f1' in fresh_html}")
            logger.info(f"Has Inter font: {'Inter' in fresh_html}")
            return HTMLResponse(content=fresh_html)
        except Exception as e:
            logger.error(f"Error reading HTML file {html_file}: {e}")
            import traceback
            traceback.print_exc()
    
    # Should never reach here, but fallback just in case
    logger.error("Could not load HTML file, using fallback")
    return HTMLResponse(content="<html><body><h1>Error: Could not load frontend</h1></body></html>")
    # Fallback HTML
    print(f"DEBUG: HTML content is None, returning fallback")
    return HTMLResponse(content=f"""
    <html>
        <head><title>AI Agent Bounty Arena</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1>AI Agent Bounty Arena API</h1>
            <p>Frontend HTML file not found at expected location.</p>
            <p><a href="/docs">View API Docs (Swagger)</a></p>
            <p style="color: #666; margin-top: 40px;">
                Expected path: {index_path or 'Not found'}<br>
                Frontend path: {frontend_path or 'Not found'}<br>
                HTML loaded: {html_content is not None}
            </p>
        </body>
    </html>
    """)

# Include routers AFTER root route
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(bounties.router, prefix="/api/bounties", tags=["Bounties"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(arenas.router, prefix="/api/arenas", tags=["Arenas"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])

@app.get("/app", response_class=HTMLResponse)
async def serve_app():
    """Serve the main frontend application"""
    if html_content:
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<html><body><h1>Frontend not found</h1></body></html>")


@app.get("/health")
async def health_check():
    """Health check endpoint with detailed database info"""
    from app.database import engine
    from sqlalchemy import text
    
    db_info = {
        "status": "healthy",
        "database": "unknown",
        "database_type": "unknown",
        "database_connected": False,
        "tables_exist": False,
        "sandbox": "ready"
    }
    
    try:
        # Check database connection and type
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql"):
            db_info["database_type"] = "PostgreSQL"
            db_info["database"] = "PostgreSQL (persistent)"
        elif db_url.startswith("sqlite"):
            db_info["database_type"] = "SQLite"
            db_info["database"] = "SQLite (NOT persistent on Railway!)"
        else:
            db_info["database_type"] = "Unknown"
            db_info["database"] = f"Unknown: {db_url[:30]}..."
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_info["database_connected"] = True
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            db_info["tables_exist"] = len(tables) > 0
            db_info["table_count"] = len(tables)
            
            # Check data counts
            if 'users' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                db_info["user_count"] = result.fetchone()[0]
            
            if 'bounties' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM bounties"))
                db_info["bounty_count"] = result.fetchone()[0]
        
        # Warn if using SQLite on Railway
        if os.getenv("RAILWAY_ENVIRONMENT") and db_url.startswith("sqlite"):
            db_info["warning"] = "Using SQLite on Railway - data will be lost! Add PostgreSQL database."
            db_info["database"] = "SQLite (⚠️ NOT PERSISTENT)"
        
    except Exception as e:
        db_info["status"] = "error"
        db_info["database"] = f"Connection failed: {str(e)[:100]}"
        db_info["database_connected"] = False
    
    return db_info


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

