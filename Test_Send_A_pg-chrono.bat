@echo off
echo.
echo ==========================================
echo Sending skiffs_A.json to pg-chrono.fr
echo ==========================================
echo.

curl.exe -X POST https://pg-chrono.fr/api/eep ^
  -H "Content-Type: application/json" ^
  --data-binary "@skiffs_A.json"

echo.
echo.
pause