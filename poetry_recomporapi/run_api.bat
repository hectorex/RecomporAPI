@echo off
cd /d "%~dp0"
poetry run uvicorn API.main:app --reload 