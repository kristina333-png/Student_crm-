from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия")
    email: EmailStr = Field(..., description="Email")
    phone: str = Field(None, max_length=20, description="Телефон")
    group_id: int = Field(None, description="ID группы")
    enrollment_date: date = Field(None, description="Дата зачисления")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: str = Field(None, min_length=1, max_length=50)
    last_name: str = Field(None, min_length=1, max_length=50)
    email: EmailStr = None
    phone: str = Field(None, max_length=20)
    group_id: int = None
    enrollment_date: date = None


class StudentResponse(StudentBase):
    id: int
    phone: str | None = None
    group_id: int | None = None
    enrollment_date: date | None = None
    group_name: str | None = None

    model_config = {"from_attributes": True}


class StudentListResponse(BaseModel):
    items: List[StudentResponse]
    total: int
    page: int
    limit: int
    pages: int