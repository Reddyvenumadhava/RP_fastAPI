from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Text, ForeignKey, Boolean, Date, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class M2MStudentSkill(Base):
    """tbl_cd_candidate_skills - Candidate skill records."""
    __tablename__ = "tbl_cd_candidate_skills"

    candidate_skill_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, nullable=False)
    skill_id = Column(Integer, nullable=False)
    proficiency_level = Column(VARCHAR(50), default='Intermediate')
    years_of_experience = Column(DECIMAL(4, 2), nullable=True)
    extracted_from_section = Column(VARCHAR(100), nullable=True)
    confidence_score = Column(DECIMAL(5, 4), default=0.5000)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class M2MStudentLanguage(Base):
    """tbl_cp_m2m_std_lng - Many-to-many relationship between students and languages."""
    __tablename__ = "tbl_cd_m2m_std_lng"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    language_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class M2MStudentInterest(Base):
    """tbl_cp_m2m_std_interest - Many-to-many relationship between students and interests."""
    __tablename__ = "tbl_cd_m2m_std_interest"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    interest_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class M2MStudentCertification(Base):
    """tbl_cd_candidate_certifications - Candidate certification records."""
    __tablename__ = "tbl_cd_candidate_certifications"

    candidate_cert_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, nullable=False)
    certification_id = Column(Integer, nullable=False)
    issue_date = Column(Date, default='1900-01-01')
    expiry_date = Column(Date, default='9999-12-31')
    credential_url = Column(VARCHAR(500), default='')
    credential_id = Column(VARCHAR(150), default='')
    is_expired = Column(Boolean, default=False)
    confidence_score = Column(DECIMAL(5, 4), default=0.5000)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class M2MProjectSkill(Base):
    """tbl_cp_m2m_studentproject_skill - Many-to-many relationship between projects and skills."""
    __tablename__ = "tbl_cd_m2m_studentproject_skill"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    skill_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
