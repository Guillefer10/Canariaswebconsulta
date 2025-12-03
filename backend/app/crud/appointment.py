from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class CRUDAppt(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):
    def get_overlapping(self, db: Session, worker_id: int, start: datetime, end: datetime, exclude_id: Optional[int] = None) -> List[Appointment]:
        query = db.query(Appointment).filter(
            Appointment.worker_id == worker_id,
            Appointment.status.notin_(
                [
                    AppointmentStatus.cancelled_by_client,
                    AppointmentStatus.cancelled_by_clinic,
                    AppointmentStatus.no_show,
                    AppointmentStatus.done,
                ]
            ),
            or_(
                and_(Appointment.start_datetime <= start, Appointment.end_datetime > start),
                and_(Appointment.start_datetime < end, Appointment.end_datetime >= end),
                and_(Appointment.start_datetime >= start, Appointment.end_datetime <= end),
            ),
        )
        if exclude_id:
            query = query.filter(Appointment.id != exclude_id)
        return query.all()

    def create(self, db: Session, obj_in: AppointmentCreate) -> Appointment:
        if obj_in.end_datetime <= obj_in.start_datetime:
            raise ValueError("Appointment end must be after start time")
        overlaps = self.get_overlapping(db, obj_in.worker_id, obj_in.start_datetime, obj_in.end_datetime)
        if overlaps:
            raise ValueError("Overlapping appointment for worker")
        return super().create(db, obj_in)

    def update(self, db: Session, db_obj: Appointment, obj_in: AppointmentUpdate | dict) -> Appointment:
        data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        start = data.get("start_datetime", db_obj.start_datetime)
        end = data.get("end_datetime", db_obj.end_datetime)
        if end <= start:
            raise ValueError("Appointment end must be after start time")
        overlaps = self.get_overlapping(db, db_obj.worker_id, start, end, exclude_id=db_obj.id)
        if overlaps:
            raise ValueError("Overlapping appointment for worker")
        return super().update(db, db_obj, data)


def _get_crud():
    return CRUDAppt(Appointment)


crud_appointment = _get_crud()
