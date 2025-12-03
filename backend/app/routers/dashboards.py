from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud.client_profile import crud_client_profile
from app.crud.user import crud_user
from app.models.appointment import Appointment, AppointmentStatus
from app.utils.exceptions import forbidden

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


def _today_bounds():
    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


@router.get("/admin")
def admin_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise forbidden("Solo administradores")

    start, end = _today_bounds()

    total_today = (
        db.query(Appointment)
        .filter(
            Appointment.start_datetime >= start,
            Appointment.start_datetime < end,
        )
        .count()
    )

    cancelled_today = (
        db.query(Appointment)
        .filter(
            Appointment.start_datetime >= start,
            Appointment.start_datetime < end,
            Appointment.status.in_(
                [AppointmentStatus.cancelled_by_client, AppointmentStatus.cancelled_by_clinic]
            ),
        )
        .count()
    )

    # Ocupacion simplificada: numero de citas por profesional hoy (excluye canceladas/no_show)
    booked_statuses = [
        AppointmentStatus.pending,
        AppointmentStatus.confirmed,
        AppointmentStatus.done,
    ]
    workers = (
        db.query(crud_user.model)
        .filter(crud_user.model.role == "worker")
        .all()
    )
    occupancy_by_worker = []
    for worker in workers:
        count = (
            db.query(Appointment)
            .filter(
                Appointment.worker_id == worker.id,
                Appointment.start_datetime >= start,
                Appointment.start_datetime < end,
                Appointment.status.in_(booked_statuses),
            )
            .count()
        )
        occupancy_by_worker.append(
            {
                "worker_id": worker.id,
                "worker_name": f"{worker.first_name} {worker.last_name}",
                "appointments_today": count,
            }
        )

    return {
        "appointments_today": total_today,
        "cancelled_today": cancelled_today,
        "occupancy_by_worker": occupancy_by_worker,
    }


@router.get("/worker")
def worker_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "worker":
        raise forbidden("Solo profesionales")

    now = datetime.utcnow()
    upcoming = (
        db.query(Appointment)
        .filter(
            Appointment.worker_id == current_user.id,
            Appointment.start_datetime >= now,
            Appointment.status.in_(
                [
                    AppointmentStatus.pending,
                    AppointmentStatus.confirmed,
                ]
            ),
        )
        .order_by(Appointment.start_datetime.asc())
        .limit(5)
        .all()
    )

    start, end = _today_bounds()
    new_clients_today = (
        db.query(crud_client_profile.model)
        .filter(
            crud_client_profile.model.join_date >= start.date(),
            crud_client_profile.model.join_date < end.date(),
        )
        .count()
    )

    return {
        "upcoming_appointments": upcoming,
        "new_clients_today": new_clients_today,
    }


@router.get("/client")
def client_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "client":
        raise forbidden("Solo clientes")

    profile = crud_client_profile.get_by_user(db, current_user.id)
    if not profile:
        return {"next_appointment": None, "last_visits": []}

    now = datetime.utcnow()

    next_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.client_id == profile.id,
            Appointment.start_datetime >= now,
            Appointment.status.in_(
                [
                    AppointmentStatus.pending,
                    AppointmentStatus.confirmed,
                ]
            ),
        )
        .order_by(Appointment.start_datetime.asc())
        .first()
    )

    last_visits = (
        db.query(Appointment)
        .filter(
            Appointment.client_id == profile.id,
            Appointment.start_datetime < now,
            Appointment.status.in_(
                [
                    AppointmentStatus.done,
                    AppointmentStatus.no_show,
                    AppointmentStatus.cancelled_by_client,
                    AppointmentStatus.cancelled_by_clinic,
                ]
            ),
        )
        .order_by(appt_model.start_datetime.desc())
        .limit(5)
        .all()
    )

    return {
        "next_appointment": next_appointment,
        "last_visits": last_visits,
    }
