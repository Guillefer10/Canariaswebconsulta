from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class AppointmentStatus(str, enum.Enum):
    pending = "pendiente"
    confirmed = "confirmada"
    cancelled = "cancelada"
    done = "realizada"


class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientprofile.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    treatment_type_id = Column(Integer, ForeignKey("treatmenttype.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)
    notes = Column(String, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    client = relationship("ClientProfile", back_populates="appointments", foreign_keys=[client_id])
    worker = relationship("User", back_populates="worker_appointments", foreign_keys=[worker_id])
    treatment_type = relationship("TreatmentType")
