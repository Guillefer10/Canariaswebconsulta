# Canariaswebconsulta

Proyecto full-stack para la gestión de una clínica de belleza/estética.

## Backend (FastAPI)

Requisitos: Python 3.11+

Instala dependencias y arranca el servidor en modo desarrollo:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Variables de entorno (ver `.env.example`):

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/beauty_clinic
JWT_SECRET=changeme
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60
```

La API expone los endpoints bajo `/api/v1` e incluye autenticación JWT, gestión de usuarios (admin), clientes, tratamientos, sesiones y citas con validaciones básicas.

## Frontend (React + Vite)

Requisitos: Node.js 20+

```bash
cd frontend
npm install
npm run dev -- --port 5173
```

Puedes configurar la URL de la API con `VITE_API_BASE_URL` (por defecto `http://localhost:8000/api/v1`). La SPA consume la API del backend y ofrece dashboards para administradores, trabajadores y clientes con rutas protegidas por rol.

### Experiencia visual y modo nocturno

La interfaz utiliza un diseño de panel limpio, con tarjetas y tablas estilizadas para cada vista. Desde la barra superior puedes alternar entre modo claro y nocturno; la preferencia se guarda en `localStorage` y respeta el esquema de color del sistema cuando es la primera carga.
