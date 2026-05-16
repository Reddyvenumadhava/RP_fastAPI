from sqlalchemy import Column, Integer, VARCHAR, DateTime, Text, Boolean, Date, DECIMAL
from database import Base
from datetime import datetime


class StudentProject(Base):
    """tbl_cd_projects - Candidate project records."""
    __tablename__ = "tbl_cd_projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, nullable=False)
    project_title = Column(VARCHAR(300), nullable=False)
    project_description = Column(Text, nullable=True)
    project_url = Column(VARCHAR(500), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)
    technologies_used = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    team_size = Column(Integer, nullable=True)
    role = Column(VARCHAR(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
