from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class GradeBase(BaseModel):
    student_id: int = Field(..., description="ID студента")
    subject: str = Field(..., min_length=1, max_length=100)
    score: float = Field(..., ge=1, le=5)
    grade_date: Optional[date] = Field(None)


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    score: Optional[float] = Field(None, ge=1, le=5)
    grade_date: Optional[date] = None


class GradeResponse(GradeBase):
    id: int

    class Config:
        from_attributes = True