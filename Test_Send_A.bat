@echo off
echo.
echo ==========================================
echo Envoi du document skiffs_A.json
echo ==========================================
echo.

curl.exe -X POST http://127.0.0.1:5000/api/eep ^
  -H "Content-Type: application/json" ^
  --data-binary "@skiffs_A.json"

echo.
echo.
pause