from pydantic import BaseModel, Field
from datetime import date
from typing import List


class GradeBase(BaseModel):
    student_id: int = Field(..., description="ID студента")
    subject: str = Field(..., min_length=1, max_length=100)
    score: float = Field(..., ge=1, le=5)
    grade_date: date = Field(None)


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    subject: str = Field(None, min_length=1, max_length=100)
    score: float = Field(None, ge=1, le=5)
    grade_date: date = None


class GradeResponse(GradeBase):
    id: int
    grade_date: date | None = None

    model_config = {"from_attributes": True}


class GradeListResponse(BaseModel):
    items: List[GradeResponse]
    total: int
    page: int
    limit: int
    pages: int