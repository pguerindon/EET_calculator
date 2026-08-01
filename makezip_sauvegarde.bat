@echo off
setlocal

cd /d "%~dp0"

echo ==========================================
echo Creation archive de sauvegarde EET
echo ==========================================

rem Lecture de la version depuis version.py
for /f %%i in ('python -c "from version import APP_VERSION; print(APP_VERSION)"') do (
    set "VER=%%i"
)

echo VER=[%VER%]

set "ZIPFILE=EET_Sauvegarde_v%VER%.zip"

if exist "%ZIPFILE%" del "%ZIPFILE%"

"C:\Program Files\7-Zip\7z.exe" a -tzip "%ZIPFILE%" @ressources_sauvegarde.lst

if errorlevel 1 (
    echo.
    echo Erreur lors de la creation de l'archive.
    pause
    exit /b 1
)

echo.
echo Archive creee :
echo %ZIPFILE%

pause