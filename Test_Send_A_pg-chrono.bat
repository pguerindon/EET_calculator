@echo off
echo.
echo ==========================================
echo Sending skiffs_A.json to pg-chrono.fr
echo ==========================================
echo.

curl.exe -X POST https://pg-chrono.fr/api/eep ^
  -H "Content-Type: application/json" ^
  --data-binary "@c:/skiFFS_utf-8/tmp/temp_EET.json"

echo.
echo.
pause