from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from app.db.base import Base


class ClinicalNote(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientprofile.id"), nullable=False, index=True)
    worker_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    episode_id = Column(Integer, ForeignKey("clinicalepisode.id"), nullable=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointment.id"), nullable=True, index=True)
    treatment_type_id = Column(Integer, ForeignKey("treatmenttype.id"), nullable=True)
    note_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    motive = Column(String, nullable=True)
    observations = Column(Text, nullable=True)
    plan = Column(Text, nullable=True)
    attachments = Column(Text, nullable=True)

    client = relationship("ClientProfile", back_populates="clinical_notes")
    worker = relationship("User", foreign_keys=[worker_id])
    episode = relationship("ClinicalEpisode", back_populates="notes")
    appointment = relationship("Appointment")
    treatment_type = relationship("TreatmentType")

    __table_args__ = (
        Index("ix_clinical_note_client_date", "client_id", "note_date"),
        Index("ix_clinical_note_episode", "episode_id"),
    )
