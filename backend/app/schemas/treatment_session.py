from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TreatmentSessionBase(BaseModel):
    client_id: int
    worker_id: int
    treatment_type_id: int
    performed_at: Optional[datetime] = None
    notes: Optional[str] = None
    products_used: Optional[str] = None
    outcome: Optional[str] = None
    attachments: Optional[str] = None


class TreatmentSessionCreate(TreatmentSessionBase):
    pass


class TreatmentSessionUpdate(BaseModel):
    performed_at: Optional[datetime] = None
    notes: Optional[str] = None
    products_used: Optional[str] = None
    outcome: Optional[str] = None
    attachments: Optional[str] = None


class TreatmentSessionRead(TreatmentSessionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
