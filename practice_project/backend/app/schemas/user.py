from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)
    full_name: str = Field(..., min_length=1)
    role: str = Field(default="student", pattern="^(admin|teacher|student)$")


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    full_name: str

    model_config = {"from_attributes": True}