@echo off
setlocal

cd /d "%~dp0"

echo ==========================================
echo Creation archive de sauvegarde EET
echo ==========================================

for /f "tokens=3 delims= " %%i in ('findstr APP_VERSION version.py') do (
    set "VER=%%~i"
)

set "VER=%VER:"=%"
set ZIPFILE=EET_Sauvegarde_v%VER%.zip

if exist "%ZIPFILE%" del "%ZIPFILE%"

"C:\Program Files\7-Zip\7z.exe" a -tzip "%ZIPFILE%" @ressources_sauvegarde.lst

if errorlevel 1 (
    echo.
    echo Erreur lors de la creation de l'archive
    pause
    exit /b 1
)

echo.
echo Archive creee :
echo %ZIPFILE%
pause