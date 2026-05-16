from sqlalchemy import Column, Integer, VARCHAR, DateTime, Text, Boolean, Date, DECIMAL
from database import Base
from datetime import datetime


class StudentWorkExp(Base):
    """tbl_cd_experience - Candidate work experience records."""
    __tablename__ = "tbl_cd_experience"

    experience_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=True)
    company_name = Column(VARCHAR(300), nullable=False)
    job_title_id = Column(Integer, nullable=True)
    job_title = Column(VARCHAR(200), nullable=False)
    employment_type = Column(VARCHAR(50), default='Full-Time')
    location = Column(VARCHAR(200), default=None)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)
    work_description = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
