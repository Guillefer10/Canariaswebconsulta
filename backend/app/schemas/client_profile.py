from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class ClientProfileBase(BaseModel):
    phone: str
    birth_date: date
    national_id: str
    address: Optional[str] = None
    medical_notes: Optional[str] = None
    consent_data: bool
    join_date: date
    skin_type: Optional[str] = None
    conditions: Optional[str] = None


class ClientProfileCreate(ClientProfileBase):
    user_id: int


class ClientProfileUpdate(BaseModel):
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    national_id: Optional[str] = None
    address: Optional[str] = None
    medical_notes: Optional[str] = None
    consent_data: Optional[bool] = None
    join_date: Optional[date] = None
    skin_type: Optional[str] = None
    conditions: Optional[str] = None


class ClientProfileRead(ClientProfileBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
