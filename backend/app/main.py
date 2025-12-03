from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
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


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
