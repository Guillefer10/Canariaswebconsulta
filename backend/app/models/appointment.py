from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from sqlalchemy import Index


class AppointmentStatus(str, enum.Enum):
    pending = "pendiente"
    confirmed = "confirmada"
    done = "realizada"
    cancelled_by_client = "cancelada_paciente"
    cancelled_by_clinic = "cancelada_clinica"
    no_show = "no_show"


class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientprofile.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    treatment_type_id = Column(Integer, ForeignKey("treatmenttype.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False, index=True)
    end_datetime = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)
    notes = Column(String, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    client = relationship("ClientProfile", back_populates="appointments", foreign_keys=[client_id])
    worker = relationship("User", back_populates="worker_appointments", foreign_keys=[worker_id])
    treatment_type = relationship("TreatmentType")

    __table_args__ = (
        Index("ix_appointment_worker_start", "worker_id", "start_datetime"),
        Index("ix_appointment_client_start", "client_id", "start_datetime"),
    )
