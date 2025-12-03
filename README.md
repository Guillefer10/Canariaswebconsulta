# Canariaswebconsulta

Plataforma full-stack para gestion de clinica (agenda, pacientes, historia clinica ligera, consentimientos y dashboards).

## Backend (FastAPI)

Requisitos: Python 3.11+

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
ENVIRONMENT=local
CORS_ORIGINS=http://localhost:5173
```

Endpoints bajo `/api/v1` con JWT, gestion de usuarios, clientes, tratamientos, sesiones y citas con reglas de negocio centralizadas en `app/services/appointment_service.py` (sin solapes, horario laboral, validaciones por rol).

Migraciones Alembic:
```bash
cd backend
alembic upgrade head  # aplica migraciones (incluye clinical/consents e índices)
alembic revision --autogenerate -m "mensaje"  # generar nuevas revisiones
```

## Frontend (React + Vite)

Requisitos: Node.js 20+

```bash
cd frontend
npm install
npm run dev -- --port 5173
```

Configura la URL de API con `VITE_API_BASE_URL` (por defecto `http://localhost:8000/api/v1`). SPA con rutas protegidas por rol y React Query para datos.

### Experiencia visual y modo nocturno

Diseño de panel con tarjetas/tablas; modo claro/oscuro con preferencia en `localStorage`.

## Resumen funcional
- Citas con estados (`pendiente`, `confirmada`, `realizada`, `cancelada_paciente`, `cancelada_clinica`, `no_show`) y transiciones validadas.
- Historia clinica ligera: episodios y notas en `/clinical/...`.
- Consentimientos RGPD en `/consents/...` (privacidad y datos de salud).
- Dashboards por rol en `/dashboards/...` (admin, worker, client).
- Frontend con servicios para citas, clinica, consentimientos y dashboards.

## Docker

Arranque completo con Postgres, backend y frontend (nginx):

```bash
docker-compose up --build
```

`VITE_API_BASE_URL` se inyecta al contenedor de frontend apuntando a `/api/v1`.

## Scripts rápidos (Windows PowerShell)
- Backend: `.\start-backend.ps1` → crea venv si falta, instala deps, aplica migraciones Alembic y levanta uvicorn en 8000.
- Frontend: `.\start-frontend.ps1` → instala deps si falta `node_modules` y arranca `npm run dev` en 5173.
