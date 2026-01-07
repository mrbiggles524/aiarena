#!/usr/bin/env python3
"""
Test script to verify Dockerfile structure
"""
import os
import sys

print("Testing Dockerfile structure...")
print("=" * 60)

# Check if files exist
files_to_check = [
    "backend/railway_start.py",
    "backend/main.py",
    "backend/requirements.txt",
    "frontend/index.html",
    "Dockerfile"
]

all_exist = True
for file in files_to_check:
    exists = os.path.exists(file)
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {file}")
    if not exists:
        all_exist = False

print("=" * 60)

# Check railway_start.py content
if os.path.exists("backend/railway_start.py"):
    with open("backend/railway_start.py", "r") as f:
        content = f.read()
        if "uvicorn" in content and "PORT" in content:
            print("[OK] railway_start.py looks correct")
        else:
            print("[ERROR] railway_start.py might have issues")
            all_exist = False

# Check Dockerfile
if os.path.exists("Dockerfile"):
    with open("Dockerfile", "r") as f:
        dockerfile = f.read()
        if "CMD" in dockerfile and "railway_start.py" in dockerfile:
            print("[OK] Dockerfile CMD looks correct")
        else:
            print("[ERROR] Dockerfile CMD might have issues")
            all_exist = False
        
        if "cd" in dockerfile.lower():
            print("[WARNING] Dockerfile contains 'cd' command!")
            all_exist = False

print("=" * 60)
if all_exist:
    print("[SUCCESS] All checks passed! Dockerfile should work.")
    sys.exit(0)
else:
    print("[FAILED] Some checks failed. Please review the issues above.")
    sys.exit(1)

