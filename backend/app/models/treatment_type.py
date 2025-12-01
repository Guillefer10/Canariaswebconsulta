from sqlalchemy import Boolean, Column, Float, Integer, String, Text

from app.db.base import Base


class TreatmentType(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    estimated_duration_minutes = Column(Integer, nullable=False)
    base_price = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
