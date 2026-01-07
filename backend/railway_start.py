#!/usr/bin/env python3
"""
Railway startup script - reads PORT from environment
"""
import os
import uvicorn

if __name__ == "__main__":
    # Railway sets PORT automatically
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level="info"
    )

