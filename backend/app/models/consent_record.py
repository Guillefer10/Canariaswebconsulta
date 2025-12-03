from datetime import datetime
import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship

from app.db.base import Base


class ConsentType(str, enum.Enum):
    privacy_policy = "privacy_policy"
    health_data = "health_data"


class ConsentRecord(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientprofile.id"), nullable=False, index=True)
    consent_type = Column(Enum(ConsentType), nullable=False)
    text_version = Column(String, nullable=False)
    accepted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    accepted_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    client = relationship("ClientProfile", back_populates="consents")
    accepted_by_user = relationship("User", foreign_keys=[accepted_by_user_id])

    __table_args__ = (
        Index("ix_consent_client_type", "client_id", "consent_type"),
    )
