# Dockerfile for AI Agent Bounty Arena
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY .env* ./

# Set working directory
WORKDIR /app/backend

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Health check (simplified - Railway has its own health checks)
# HEALTHCHECK removed - Railway handles this

# Run the application
# Use Python script to read PORT from Railway environment
CMD ["python", "railway_start.py"]

