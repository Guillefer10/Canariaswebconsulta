from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.consent_record import ConsentType


class ConsentRecordBase(BaseModel):
    client_id: Optional[int] = None
    consent_type: ConsentType
    text_version: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    accepted_by_user_id: Optional[int] = None


class ConsentRecordCreate(ConsentRecordBase):
    pass


class ConsentRecordRead(ConsentRecordBase):
    id: int
    client_id: int
    accepted_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
