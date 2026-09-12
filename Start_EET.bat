@echo off
setlocal

cd /d "%~dp0"

set EET_SECRET_KEY=CLE_SECRETE_WINDOWS

call venv\Scripts\activate

python run.py

pause