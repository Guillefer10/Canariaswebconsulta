from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.utils.logging import get_logger
from app.routers import auth, users, clients, treatments, sessions, appointments, clinical, dashboards, consents

app = FastAPI(title=settings.app_name, openapi_url="/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(treatments.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(appointments.router, prefix="/api/v1")
app.include_router(clinical.router, prefix="/api/v1")
app.include_router(dashboards.router, prefix="/api/v1")
app.include_router(consents.router, prefix="/api/v1")

logger = get_logger("app.request")


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("HTTP %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("HTTP %s %s -> %s", request.method, request.url.path, response.status_code)
    return response


@app.get("/api/v1/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check que valida conexion a base de datos.
    """
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return {"status": "ok" if db_ok else "degraded", "db": db_ok}
