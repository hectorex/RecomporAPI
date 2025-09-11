@echo off
"%~dp0.venv\Scripts\python.exe" -m uvicorn API.main:app --reload
