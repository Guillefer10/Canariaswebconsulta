from datetime import datetime, timedelta
from typing import Iterable
from sqlalchemy.orm import Session

from app.crud.appointment import crud_appointment
from app.crud.client_profile import crud_client_profile
from app.crud.treatment_type import crud_treatment_type
from app.crud.user import crud_user
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentReschedule, AppointmentUpdate
from app.utils.exceptions import bad_request, forbidden, not_found
from app.utils.validators import ensure_worker


class AppointmentService:
    def __init__(self, now_provider=datetime.utcnow):
        self.now = now_provider

    def list(
        self,
        db: Session,
        current_user,
        start: datetime | None,
        end: datetime | None,
        worker_id: int | None,
        client_id: int | None,
    ) -> Iterable[Appointment]:
        query = db.query(crud_appointment.model)
        if current_user.role == "worker":
            query = query.filter(crud_appointment.model.worker_id == current_user.id)
        if current_user.role == "client":
            profile = crud_client_profile.get_by_user(db, current_user.id)
            if not profile:
                return []
            query = query.filter(crud_appointment.model.client_id == profile.id)
        if worker_id:
            query = query.filter(crud_appointment.model.worker_id == worker_id)
        if client_id:
            query = query.filter(crud_appointment.model.client_id == client_id)
        if start:
            query = query.filter(crud_appointment.model.start_datetime >= start)
        if end:
            query = query.filter(crud_appointment.model.end_datetime <= end)
        return query.all()

    def create(self, db: Session, data: AppointmentCreate, current_user) -> Appointment:
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

        end_time = data.end_datetime or data.start_datetime + timedelta(minutes=treatment.estimated_duration_minutes)
        now = self.now()
        if data.start_datetime < now and current_user.role != "admin":
            raise bad_request("No se puede crear una cita en el pasado")

        self._validate_worker_hours(data.start_datetime, end_time)
        self._ensure_no_overlap(db, data.worker_id, data.start_datetime, end_time)

        status = AppointmentStatus.pending
        if current_user.role == "admin" and data.start_datetime < now:
            if data.status not in (AppointmentStatus.done, AppointmentStatus.no_show):
                raise bad_request("Para registrar citas pasadas, usa estado realizada o no_show")
            status = data.status

        payload = data.model_dump()
        payload["end_datetime"] = end_time
        payload["created_by_user_id"] = current_user.id
        payload["status"] = status

        try:
            return crud_appointment.create(db, AppointmentCreate(**payload))
        except ValueError as ex:
            raise bad_request(str(ex))

    def update(self, db: Session, appointment_id: int, data: AppointmentUpdate, current_user) -> Appointment:
        appointment = self._get_appointment(db, appointment_id)

        if current_user.role == "client":
            raise forbidden("Los clientes solo pueden cancelar sus citas")
        if current_user.role == "worker" and appointment.worker_id != current_user.id:
            raise forbidden("No autorizado")

        now = self.now()
        is_reschedule = data.start_datetime is not None or data.end_datetime is not None

        new_start = data.start_datetime or appointment.start_datetime
        new_end = data.end_datetime or appointment.end_datetime

        if appointment.start_datetime < now and is_reschedule:
            raise bad_request("No se puede reprogramar una cita pasada")
        if data.start_datetime and data.start_datetime < now and current_user.role != "admin":
            raise bad_request("No se puede mover una cita al pasado")

        if data.status is not None:
            self._validate_status_transition(appointment.status, data.status, current_user.role, appointment.start_datetime)

        if is_reschedule:
            self._validate_worker_hours(new_start, new_end)
            self._ensure_no_overlap(db, appointment.worker_id, new_start, new_end, exclude_id=appointment.id)

        try:
            return crud_appointment.update(db, appointment, data)
        except ValueError as ex:
            raise bad_request(str(ex))

    def change_status(self, db: Session, appointment_id: int, data: AppointmentUpdate, current_user) -> Appointment:
        appointment = self._get_appointment(db, appointment_id)

        if data.status is None:
            raise bad_request("Estado requerido")

        self._validate_status_transition(appointment.status, data.status, current_user.role, appointment.start_datetime)

        try:
            return crud_appointment.update(db, appointment, {"status": data.status})
        except ValueError as ex:
            raise bad_request(str(ex))

    def reschedule(self, db: Session, appointment_id: int, data: AppointmentReschedule, current_user) -> Appointment:
        appointment = self._get_appointment(db, appointment_id)

        if current_user.role == "client":
            raise forbidden("No autorizado para reprogramar")
        if current_user.role == "worker" and appointment.worker_id != current_user.id:
            raise forbidden("No autorizado para reprogramar")
        if appointment.start_datetime < self.now():
            raise bad_request("No se puede reprogramar una cita pasada")

        new_end = data.end_datetime or appointment.end_datetime

        if data.start_datetime < self.now() and current_user.role != "admin":
            raise bad_request("No se puede mover una cita al pasado")

        self._validate_worker_hours(data.start_datetime, new_end)
        self._ensure_no_overlap(db, appointment.worker_id, data.start_datetime, new_end, exclude_id=appointment.id)

        try:
            return crud_appointment.update(
                db,
                appointment,
                {"start_datetime": data.start_datetime, "end_datetime": new_end},
            )
        except ValueError as ex:
            raise bad_request(str(ex))

    def cancel(self, db: Session, appointment_id: int, current_user) -> Appointment:
        appointment = self._get_appointment(db, appointment_id)
        status = AppointmentStatus.cancelled_by_clinic

        if current_user.role == "client":
            profile = crud_client_profile.get_by_user(db, current_user.id)
            if not profile or appointment.client_id != profile.id:
                raise forbidden("No autorizado")
            status = AppointmentStatus.cancelled_by_client

        if current_user.role == "worker" and appointment.worker_id != current_user.id:
            raise forbidden("No autorizado")

        try:
            return crud_appointment.update(db, appointment, {"status": status})
        except ValueError as ex:
            raise bad_request(str(ex))

    def _get_appointment(self, db: Session, appointment_id: int) -> Appointment:
        appointment = crud_appointment.get(db, appointment_id)
        if not appointment:
            raise not_found("Appointment")
        return appointment

    def _validate_worker_hours(self, start: datetime, end: datetime):
        """
        Validacion basica de horario: evita fuera de 08:00-20:00 y fines de semana.
        Sustituir por validacion real de agenda del profesional cuando se modele.
        """
        if start.weekday() >= 6:
            raise bad_request("No se pueden crear citas en fin de semana")
        if not (8 <= start.hour < 20 and 8 <= end.hour <= 20):
            raise bad_request("Cita fuera del horario laboral (08:00-20:00)")

    def _validate_status_transition(
        self, current_status: AppointmentStatus, new_status: AppointmentStatus | None, role: str, start_datetime: datetime
    ):
        if new_status is None or new_status == current_status:
            return

        is_future = start_datetime > self.now()

        allowed = {
            "admin": {
                AppointmentStatus.pending: {
                    AppointmentStatus.confirmed,
                    AppointmentStatus.done,
                    AppointmentStatus.no_show,
                    AppointmentStatus.cancelled_by_client,
                    AppointmentStatus.cancelled_by_clinic,
                },
                AppointmentStatus.confirmed: {
                    AppointmentStatus.done,
                    AppointmentStatus.no_show,
                    AppointmentStatus.cancelled_by_client,
                    AppointmentStatus.cancelled_by_clinic,
                },
            },
            "worker": {
                AppointmentStatus.pending: {
                    AppointmentStatus.confirmed,
                    AppointmentStatus.cancelled_by_clinic,
                    AppointmentStatus.cancelled_by_client,
                },
                AppointmentStatus.confirmed: {
                    AppointmentStatus.done,
                    AppointmentStatus.no_show,
                    AppointmentStatus.cancelled_by_clinic,
                    AppointmentStatus.cancelled_by_client,
                },
            },
            "client": {
                AppointmentStatus.pending: {AppointmentStatus.cancelled_by_client},
                AppointmentStatus.confirmed: {AppointmentStatus.cancelled_by_client},
            },
        }

        role_allowed = allowed.get(role, {})
        if new_status not in role_allowed.get(current_status, set()):
            raise bad_request("Transicion de estado no permitida para este rol")
        if new_status == AppointmentStatus.done and is_future:
            raise bad_request("No se puede marcar como realizada una cita futura")
        if new_status == AppointmentStatus.no_show and is_future:
            raise bad_request("No se puede marcar no_show en el futuro")

    def _ensure_no_overlap(self, db: Session, worker_id: int, start: datetime, end: datetime, exclude_id: int | None = None):
        overlaps = crud_appointment.get_overlapping(db, worker_id, start, end, exclude_id=exclude_id)
        if overlaps:
            raise bad_request("Solape con otra cita del profesional")


appointment_service = AppointmentService()
