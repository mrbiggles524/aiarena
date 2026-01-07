# Dockerfile for AI Agent Bounty Arena
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# Copy backend files directly to /app/backend (not /app/backend/backend)
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY .env* ./

# Set working directory to backend (where main.py and railway_start.py are)
WORKDIR /app/backend

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Health check (simplified - Railway has its own health checks)
# HEALTHCHECK removed - Railway handles this

# Run the application
# Railway sets PORT automatically - use shell form to read env var
# This is more reliable than the Python script
CMD python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

