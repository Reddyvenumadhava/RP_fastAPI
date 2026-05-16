from pydantic import BaseModel, field_validator
from typing import Optional


class SaveSchoolRequest(BaseModel):
    student_id: int
    standard: str                          # "10th" or "12th"
    board: Optional[str] = None
    school_name: Optional[str] = None
    percentage: Optional[float] = None
    passing_year: Optional[int] = None
    grading_system: Optional[str] = None
    score_obtained: Optional[float] = None
    maximum_score: Optional[float] = None

    @field_validator('percentage', mode='before')
    @classmethod
    def clean_percentage(cls, v):
        if isinstance(v, str):
            v = v.replace('%', '').strip()
            if not v:
                return None
            try:
                return float(v)
            except ValueError:
                return None
        return v


class SaveSchoolResponse(BaseModel):
    school_id: int


class SaveEducationRequest(BaseModel):
    student_id: int
    institution_name: str
    degree: str
    field_of_study: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_pursuing: Optional[bool] = None
    grading_system: Optional[str] = None
    score_obtained: Optional[float] = None
    maximum_score: Optional[float] = None

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def clean_dates(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            value = v.strip()
            return value or None
        return v

    @field_validator('score_obtained', 'maximum_score', mode='before')
    @classmethod
    def clean_floats(cls, v):
        if isinstance(v, str):
            value = v.replace('%', '').strip()
            if not value:
                return None
            try:
                return float(value)
            except ValueError:
                return None
        return v


class SaveEducationResponse(BaseModel):
    edu_id: int
