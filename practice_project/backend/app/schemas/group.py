from pydantic import BaseModel, Field
from typing import Optional


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class GroupResponse(GroupBase):
    id: int
    student_count: int = 0

    class Config:
        from_attributes = True