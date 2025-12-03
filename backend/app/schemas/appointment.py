from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    client_id: int
    worker_id: int
    treatment_type_id: int
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    status: AppointmentStatus = AppointmentStatus.pending
    notes: Optional[str] = None
    created_by_user_id: Optional[int] = None

    @field_validator("end_datetime")
    @classmethod
    def validate_range(cls, end: datetime | None, values: dict) -> datetime | None:
        start = values.get("start_datetime")
        if end and start and end <= start:
            raise ValueError("End datetime must be after start datetime")
        return end


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None


class AppointmentReschedule(BaseModel):
    start_datetime: datetime
    end_datetime: Optional[datetime] = None


class AppointmentRead(AppointmentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
