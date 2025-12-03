from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class ClientProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    phone = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    national_id = Column(String, nullable=False)
    address = Column(String, nullable=True)
    medical_notes = Column(Text, nullable=True)
    consent_data = Column(Boolean, nullable=False, default=False)
    join_date = Column(Date, nullable=False)
    skin_type = Column(String, nullable=True)
    conditions = Column(Text, nullable=True)

    user = relationship("User", back_populates="client_profile")
    treatment_sessions = relationship("TreatmentSession", back_populates="client")
    appointments = relationship("Appointment", back_populates="client")
    clinical_episodes = relationship("ClinicalEpisode", back_populates="client")
    clinical_notes = relationship("ClinicalNote", back_populates="client")
    consents = relationship("ConsentRecord", back_populates="client")
