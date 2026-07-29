from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database.db import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    gmail_message_id = Column(String, unique=True, index=True, nullable=False)
    thread_id = Column(String, index=True, nullable=True)
    sender = Column(String, index=True, nullable=True)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    received_at = Column(DateTime, nullable=True)
    is_processed = Column(Boolean, default=False, nullable=False)

    # One-to-one relationship to EmailAnalysis
    analysis = relationship(
        "EmailAnalysis",
        uselist=False,
        back_populates="email",
        cascade="all, delete-orphan",
    )