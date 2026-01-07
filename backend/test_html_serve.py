"""Test what HTML the server is actually serving"""
import requests
import os
from pathlib import Path

# Test direct file read
frontend_file = Path("C:/AIArena/frontend/index.html")
if frontend_file.exists():
    content = frontend_file.read_text(encoding='utf-8')
    print("=" * 60)
    print("FILE ON DISK:")
    print("=" * 60)
    print(f"Size: {len(content)} bytes")
    print(f"Has #6366f1: {'#6366f1' in content}")
    print(f"Has Inter: {'Inter' in content}")
    print(f"Has backdrop-filter: {'backdrop-filter' in content}")
    print()

# Test server response
try:
    r = requests.get('http://localhost:8000/', timeout=5)
    print("=" * 60)
    print("SERVER RESPONSE:")
    print("=" * 60)
    print(f"Status: {r.status_code}")
    print(f"Size: {len(r.text)} bytes")
    print(f"Has #6366f1: {'#6366f1' in r.text}")
    print(f"Has Inter: {'Inter' in r.text}")
    print(f"Has backdrop-filter: {'backdrop-filter' in r.text}")
    print()
    
    if len(r.text) != len(content):
        print("=" * 60)
        print("MISMATCH DETECTED!")
        print("=" * 60)
        print(f"File on disk: {len(content)} bytes")
        print(f"Server serving: {len(r.text)} bytes")
        print(f"Difference: {len(content) - len(r.text)} bytes")
        print()
        print("First 200 chars from server:")
        print(r.text[:200])
        print()
        print("First 200 chars from file:")
        print(content[:200])
except Exception as e:
    print(f"Error connecting to server: {e}")

