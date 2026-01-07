"""
Stop all running AI Arena servers
"""
import os
import sys
import subprocess
import signal

def kill_servers():
    """Kill all processes running on port 8000"""
    print("Stopping AI Agent Bounty Arena servers...")
    
    try:
        # Find processes using port 8000
        if sys.platform == 'win32':
            # Windows
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True
            )
            
            pids = set()
            for line in result.stdout.split('\n'):
                if ':8000' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[-1]
                        try:
                            pids.add(int(pid))
                        except ValueError:
                            pass
            
            # Also find Python processes that might be running the server
            result2 = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True
            )
            
            for line in result2.stdout.split('\n')[1:]:  # Skip header
                if 'python.exe' in line.lower():
                    try:
                        # Extract PID from CSV
                        parts = line.split('","')
                        if len(parts) > 1:
                            pid_str = parts[1].strip('"')
                            pid = int(pid_str)
                            # Check if it's our server by checking command line
                            try:
                                proc = subprocess.run(
                                    ['wmic', 'process', 'where', f'ProcessId={pid}', 'get', 'CommandLine', '/format:list'],
                                    capture_output=True,
                                    text=True,
                                    timeout=2
                                )
                                if 'start_server.py' in proc.stdout or 'main.py' in proc.stdout or 'uvicorn' in proc.stdout:
                                    pids.add(pid)
                            except:
                                pass
                    except (ValueError, IndexError):
                        pass
            
            # Kill all found processes
            killed = 0
            for pid in pids:
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"  Stopped process {pid}")
                    killed += 1
                except (ProcessLookupError, PermissionError, OSError) as e:
                    try:
                        # Try force kill
                        subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                                     capture_output=True, timeout=2)
                        print(f"  Force stopped process {pid}")
                        killed += 1
                    except:
                        pass
            
            if killed > 0:
                print(f"\n[OK] Stopped {killed} server process(es)")
            else:
                print("\n[OK] No server processes found running on port 8000")
                
        else:
            # Linux/Mac
            result = subprocess.run(
                ['lsof', '-ti:8000'],
                capture_output=True,
                text=True
            )
            
            pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid]
            
            killed = 0
            for pid in pids:
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"  Stopped process {pid}")
                    killed += 1
                except (ProcessLookupError, PermissionError):
                    pass
            
            if killed > 0:
                print(f"\n[OK] Stopped {killed} server process(es)")
            else:
                print("\n[OK] No server processes found running on port 8000")
                
    except Exception as e:
        print(f"Error stopping servers: {e}")
        print("\nTrying alternative method...")
        
        # Alternative: Kill all Python processes (more aggressive)
        try:
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/FI', 'WINDOWTITLE eq *uvicorn*'],
                             capture_output=True, timeout=5)
            print("[OK] Attempted to stop all server processes")
        except:
            print("[WARNING] Could not automatically stop servers")
            print("  Please manually stop them using Task Manager or:")
            print("  taskkill /F /IM python.exe")

if __name__ == "__main__":
    try:
        kill_servers()
        input("\nPress Enter to exit...")
    except (EOFError, KeyboardInterrupt):
        # Handle when run non-interactively
        pass

