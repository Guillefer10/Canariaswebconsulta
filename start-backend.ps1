$ErrorActionPreference = "Stop"

Push-Location backend

if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual .venv..."
    python -m venv .venv
}

Write-Host "Instalando dependencias backend..."
& .\.venv\Scripts\python -m pip install --upgrade pip
& .\.venv\Scripts\pip install -r requirements.txt

Write-Host "Aplicando migraciones Alembic..."
& .\.venv\Scripts\alembic upgrade head

Write-Host "Iniciando backend en http://localhost:8000 ..."
& .\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Pop-Location
