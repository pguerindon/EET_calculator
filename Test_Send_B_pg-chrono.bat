@echo off
echo.
echo ==========================================
echo Sending skiffs_B.json to pg-chrono.fr
echo ==========================================
echo.

curl.exe -X POST https://pg-chrono.fr/api/eep ^
  -H "Content-Type: application/json" ^
  --data-binary "@skiffs_B.json"

echo.
echo.
pause