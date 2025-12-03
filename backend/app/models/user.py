from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    worker = "worker"
    client = "client"


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)

    client_profile = relationship("ClientProfile", back_populates="user", uselist=False)
    worker_sessions = relationship("TreatmentSession", back_populates="worker", foreign_keys="TreatmentSession.worker_id")
    worker_appointments = relationship("Appointment", back_populates="worker", foreign_keys="Appointment.worker_id")
    clinical_notes = relationship("ClinicalNote", foreign_keys="ClinicalNote.worker_id")
    accepted_consents = relationship("ConsentRecord", foreign_keys="ConsentRecord.accepted_by_user_id")
