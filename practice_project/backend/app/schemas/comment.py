from datetime import datetime
from pydantic import BaseModel


class CommentCreate(BaseModel):
    author_name: str
    text: str


class CommentResponse(BaseModel):
    id: int
    student_id: int
    author_name: str
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}