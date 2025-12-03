from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class ClinicalEpisodeBase(BaseModel):
    client_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    is_active: bool = True

    @field_validator("closed_at")
    @classmethod
    def validate_dates(cls, closed: datetime | None, values: dict) -> datetime | None:
        start = values.get("started_at")
        if closed and start and closed < start:
            raise ValueError("closed_at cannot be before started_at")
        return closed


class ClinicalEpisodeCreate(ClinicalEpisodeBase):
    created_by_user_id: Optional[int] = None


class ClinicalEpisodeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    is_active: Optional[bool] = None

    @field_validator("closed_at")
    @classmethod
    def validate_dates(cls, closed: datetime | None, values: dict) -> datetime | None:
        start = values.get("started_at")
        if closed and start and closed < start:
            raise ValueError("closed_at cannot be before started_at")
        return closed


class ClinicalEpisodeRead(ClinicalEpisodeBase):
    client_id: int
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
