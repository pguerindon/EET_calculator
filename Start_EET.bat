@echo off
setlocal

set EET_ADMIN_SEARCH_CODE=CODE_ADMIN_TEST

cd /d "%~dp0"

set EET_SECRET_KEY=CLE_SECRETE_WINDOWS

call venv\Scripts\activate

python run.py

pause