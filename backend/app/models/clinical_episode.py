from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from app.db.base import Base


class ClinicalEpisode(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientprofile.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    client = relationship("ClientProfile", back_populates="clinical_episodes")
    notes = relationship("ClinicalNote", back_populates="episode")

    __table_args__ = (
        Index("ix_clinical_episode_client_active", "client_id", "is_active"),
        Index("ix_clinical_episode_start", "started_at"),
    )
