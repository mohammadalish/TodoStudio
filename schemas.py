from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    priority: int = Field(gt=0, lt=6)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    complete: bool


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    role: str


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
