@echo off
"%~dp0.venv\Scripts\python.exe" -m uvicorn API.main:app --host 0.0.0.0 --port 8000
