from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate, AppointmentReschedule
from app.services.appointment_service import appointment_service

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(
    start: datetime | None = Query(None),
    end: datetime | None = Query(None),
    worker_id: int | None = Query(None),
    client_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return appointment_service.list(db, current_user, start, end, worker_id, client_id)


@router.post("/", response_model=AppointmentRead)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return appointment_service.create(db, data, current_user)


@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return appointment_service.update(db, appointment_id, data, current_user)


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
def change_status(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return appointment_service.change_status(db, appointment_id, payload, current_user)


@router.patch("/{appointment_id}/reschedule", response_model=AppointmentRead)
def reschedule_appointment(
    appointment_id: int,
    payload: AppointmentReschedule,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return appointment_service.reschedule(db, appointment_id, payload, current_user)


@router.patch("/{appointment_id}/cancel", response_model=AppointmentRead)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return appointment_service.cancel(db, appointment_id, current_user)
