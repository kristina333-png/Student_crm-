from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Телефон")
    group_id: Optional[int] = Field(None, description="ID группы")
    enrollment_date: Optional[date] = Field(None, description="Дата зачисления")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    group_id: Optional[int] = None
    enrollment_date: Optional[date] = None


class StudentResponse(StudentBase):
    id: int
    group_name: Optional[str] = None

    class Config:
        from_attributes = True