"""
Simple server startup script
"""
import uvicorn
import sys
import os
import signal
import atexit

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Global reference to server
server_process = None

def cleanup():
    """Cleanup function to ensure server stops"""
    global server_process
    if server_process:
        try:
            server_process.terminate()
        except:
            pass

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n[STOP] Stopping server...")
    cleanup()
    sys.exit(0)

# Register signal handlers
if sys.platform != 'win32':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
else:
    # Windows signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

# Register cleanup on exit
atexit.register(cleanup)

if __name__ == "__main__":
    print("=" * 60)
    print("Starting AI Agent Bounty Arena Server...")
    print("=" * 60)
    print("Server: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("To stop: Press Ctrl+C (or run stop_server.py)")
    print("=" * 60)
    print()
    
    # Get port from environment (for production) or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")  # 0.0.0.0 for production, 127.0.0.1 for local
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n[OK] Server stopped by user")
        cleanup()
    except Exception as e:
        print(f"\n[ERROR] Error starting server: {e}")
        import traceback
        traceback.print_exc()
        cleanup()

