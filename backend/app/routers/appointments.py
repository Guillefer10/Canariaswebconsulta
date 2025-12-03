from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud.appointment import crud_appointment
from app.crud.client_profile import crud_client_profile
from app.crud.treatment_type import crud_treatment_type
from app.crud.user import crud_user
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate
from app.models.appointment import AppointmentStatus
from app.utils.exceptions import not_found, bad_request, forbidden
from app.utils.validators import ensure_worker

router = APIRouter(prefix="/appointments", tags=["appointments"])


def _filter_query(db: Session, user, start: datetime | None, end: datetime | None, worker_id: int | None, client_id: int | None):
    query = db.query(crud_appointment.model)
    if user.role == "worker":
        query = query.filter(crud_appointment.model.worker_id == user.id)
    if user.role == "client":
        profile = crud_client_profile.get_by_user(db, user.id)
        if not profile:
            return query.filter(False)
        query = query.filter(crud_appointment.model.client_id == profile.id)
    if worker_id:
        query = query.filter(crud_appointment.model.worker_id == worker_id)
    if client_id:
        query = query.filter(crud_appointment.model.client_id == client_id)
    if start:
        query = query.filter(crud_appointment.model.start_datetime >= start)
    if end:
        query = query.filter(crud_appointment.model.end_datetime <= end)
    return query


def _validate_status_transition(current_status: AppointmentStatus, new_status: AppointmentStatus | None, role: str):
    if new_status is None or new_status == current_status:
        return

    allowed = {
        "admin": {
            AppointmentStatus.pending: {AppointmentStatus.confirmed, AppointmentStatus.cancelled},
            AppointmentStatus.confirmed: {AppointmentStatus.done, AppointmentStatus.cancelled},
        },
        "worker": {
            AppointmentStatus.pending: {AppointmentStatus.confirmed, AppointmentStatus.cancelled},
            AppointmentStatus.confirmed: {AppointmentStatus.done, AppointmentStatus.cancelled},
        },
    }

    role_allowed = allowed.get(role, {})
    if new_status not in role_allowed.get(current_status, set()):
        raise bad_request("Transicion de estado no permitida para este rol")


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(
    start: datetime | None = Query(None),
    end: datetime | None = Query(None),
    worker_id: int | None = Query(None),
    client_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = _filter_query(db, current_user, start, end, worker_id, client_id)
    return query.all()


@router.post("/", response_model=AppointmentRead)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == "client":
        profile = crud_client_profile.get_by_user(db, current_user.id)
        if not profile or profile.id != data.client_id:
            raise forbidden("No puedes crear citas para otros clientes")
    client_profile = crud_client_profile.get(db, data.client_id)
    if not client_profile:
        raise not_found("ClientProfile")
    worker = crud_user.get(db, data.worker_id)
    if not worker:
        raise not_found("Worker")
    ensure_worker(worker)
    treatment = crud_treatment_type.get(db, data.treatment_type_id)
    if not treatment:
        raise not_found("TreatmentType")
    if data.start_datetime < datetime.utcnow():
        raise bad_request("No se puede crear una cita en el pasado")

    end_time = data.end_datetime
    if not end_time:
        end_time = data.start_datetime + timedelta(minutes=treatment.estimated_duration_minutes)
    payload = data.model_dump()
    payload["end_datetime"] = end_time
    payload["created_by_user_id"] = current_user.id
    payload["status"] = AppointmentStatus.pending
    try:
        return crud_appointment.create(db, AppointmentCreate(**payload))
    except ValueError as ex:
        raise bad_request(str(ex))


@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appointment = crud_appointment.get(db, appointment_id)
    if not appointment:
        raise not_found("Appointment")
    if current_user.role == "client":
        raise forbidden("Los clientes solo pueden cancelar sus citas")
    if current_user.role == "worker" and appointment.worker_id != current_user.id:
        raise forbidden("No autorizado")
    _validate_status_transition(appointment.status, data.status, current_user.role)
    try:
        return crud_appointment.update(db, appointment, data)
    except ValueError as ex:
        raise bad_request(str(ex))


@router.patch("/{appointment_id}/cancel", response_model=AppointmentRead)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appointment = crud_appointment.get(db, appointment_id)
    if not appointment:
        raise not_found("Appointment")
    if current_user.role == "client":
        profile = crud_client_profile.get_by_user(db, current_user.id)
        if not profile or appointment.client_id != profile.id:
            raise forbidden("No autorizado")
    if current_user.role == "worker" and appointment.worker_id != current_user.id:
        raise forbidden("No autorizado")
    return crud_appointment.update(db, appointment, {"status": AppointmentStatus.cancelled})
