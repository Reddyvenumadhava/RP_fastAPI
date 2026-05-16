from sqlalchemy import Column, Integer, VARCHAR, DateTime, Text, Boolean, DECIMAL, Enum
from database import Base
from datetime import datetime


class Student(Base):
    """tbl_cd_candidates - Candidate profile records."""
    __tablename__ = "tbl_cd_candidates"

    candidate_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    phone = Column(VARCHAR(20), unique=True, nullable=True)
    first_name = Column(VARCHAR(100), nullable=False)
    middle_name = Column(VARCHAR(100), default='')
    last_name = Column(VARCHAR(100), default='')
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(VARCHAR(20), default='Prefer Not to Say')
    work_status = Column(Enum('experienced', 'fresher', name='work_status_enum'), nullable=False, default='fresher')
    total_experience_years = Column(DECIMAL(4, 2), default=0.00)
    current_location = Column(VARCHAR(200), default=None)
    willing_to_relocate = Column(Boolean, default=False)
    linkedin_url = Column(VARCHAR(500), default=None)
    github_url = Column(VARCHAR(500), default=None)
    portfolio_url = Column(VARCHAR(500), default=None)
    profile_summary = Column(Text, default=None)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
