from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.db import Base


class EmailAnalysis(Base):
    __tablename__ = "email_analysis"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), unique=True, nullable=False)

    category = Column(String, nullable=True)  # NEW
    company = Column(String, nullable=True)
    role = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    eligibility = Column(Text, nullable=True)
    registration_link = Column(String, nullable=True)
    summary = Column(Text, nullable=True)

    processed_at = Column(DateTime, nullable=True)

    email = relationship("Email", back_populates="analysis")