#!/bin/bash
# Railway startup script
# Reads PORT from environment (Railway sets this automatically)

PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

echo "Starting server on $HOST:$PORT"
exec uvicorn main:app --host "$HOST" --port "$PORT"

