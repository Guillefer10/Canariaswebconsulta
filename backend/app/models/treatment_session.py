from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class TreatmentSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientprofile.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    treatment_type_id = Column(Integer, ForeignKey("treatmenttype.id"), nullable=False)
    performed_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    products_used = Column(Text, nullable=True)
    outcome = Column(Text, nullable=True)
    attachments = Column(Text, nullable=True)

    client = relationship("ClientProfile", back_populates="treatment_sessions")
    worker = relationship("User", back_populates="worker_sessions")
    treatment_type = relationship("TreatmentType")
