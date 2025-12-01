from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TreatmentTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    estimated_duration_minutes: int
    base_price: Optional[float] = None
    is_active: bool = True


class TreatmentTypeCreate(TreatmentTypeBase):
    pass


class TreatmentTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None
    base_price: Optional[float] = None
    is_active: Optional[bool] = None


class TreatmentTypeRead(TreatmentTypeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
