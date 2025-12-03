$ErrorActionPreference = "Stop"

Push-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependencias frontend..."
    npm install
}

Write-Host "Iniciando frontend en http://localhost:5173 ..."
npm run dev -- --host 0.0.0.0 --port 5173

Pop-Location
