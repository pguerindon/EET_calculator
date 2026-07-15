Write-Host ""
Write-Host "=== Envoi du JSON ==="

Invoke-RestMethod `
    -Uri "http://localhost:5000/api/load" `
    -Method POST `
    -ContentType "application/json" `
    -InFile ".\document.json"

Write-Host ""
Write-Host "=== Ouverture de l'application ==="

Start-Process "http://localhost:5000"