"""Test if frontend HTML can be loaded"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load frontend HTML
possible_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),
    os.path.join(os.path.dirname(__file__), "..", "frontend"),
    "C:\\AIArena\\frontend",
]

frontend_path = None
index_path = None
html_content = None

for path in possible_paths:
    abs_path = os.path.abspath(path)
    test_index = os.path.join(abs_path, "index.html")
    if os.path.exists(test_index):
        frontend_path = abs_path
        index_path = test_index
        print(f"Found frontend at: {frontend_path}")
        break

if index_path and os.path.exists(index_path):
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"Frontend HTML loaded successfully ({len(html_content)} characters)")
        print(f"First 100 chars: {html_content[:100]}")
        print(f"HTML content is not None: {html_content is not None}")
    except Exception as e:
        print(f"Error reading frontend HTML: {e}")
        html_content = None
else:
    print(f"Frontend not found. Tried paths: {possible_paths}")

# Test FastAPI route
print("\n" + "="*50)
print("Testing FastAPI import...")
try:
    from main import app, html_content as main_html_content
    print(f"FastAPI app imported successfully")
    print(f"HTML content in main module: {main_html_content is not None}")
    if main_html_content:
        print(f"HTML content length in main: {len(main_html_content)}")
    
    # Check routes
    routes = [route.path for route in app.routes]
    print(f"Available routes: {routes[:10]}...")  # First 10 routes
    if "/" in routes:
        print("Root route (/) is registered!")
    else:
        print("Root route (/) is NOT registered!")
        
except Exception as e:
    print(f"Error importing main: {e}")
    import traceback
    traceback.print_exc()

