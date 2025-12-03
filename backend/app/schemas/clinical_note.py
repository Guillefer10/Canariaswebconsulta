from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClinicalNoteBase(BaseModel):
    client_id: Optional[int] = None
    worker_id: int
    episode_id: Optional[int] = None
    appointment_id: Optional[int] = None
    treatment_type_id: Optional[int] = None
    note_date: Optional[datetime] = None
    motive: Optional[str] = None
    observations: Optional[str] = None
    plan: Optional[str] = None
    attachments: Optional[str] = None


class ClinicalNoteCreate(ClinicalNoteBase):
    pass


class ClinicalNoteUpdate(BaseModel):
    episode_id: Optional[int] = None
    appointment_id: Optional[int] = None
    treatment_type_id: Optional[int] = None
    note_date: Optional[datetime] = None
    motive: Optional[str] = None
    observations: Optional[str] = None
    plan: Optional[str] = None
    attachments: Optional[str] = None


class ClinicalNoteRead(ClinicalNoteBase):
    client_id: int
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
