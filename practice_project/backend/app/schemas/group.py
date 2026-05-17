from pydantic import BaseModel, Field
from typing import List


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(None)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = None


class GroupResponse(GroupBase):
    id: int
    student_count: int = 0
    description: str | None = None

    model_config = {"from_attributes": True}


class GroupListResponse(BaseModel):
    items: List[GroupResponse]
    total: int
    page: int
    limit: int
    pages: int