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
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY .env* ./

# Set working directory to backend (where main.py and railway_start.py are)
WORKDIR /app/backend

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application using exec form (most reliable)
# railway_start.py reads PORT from environment automatically
CMD ["python", "railway_start.py"]
