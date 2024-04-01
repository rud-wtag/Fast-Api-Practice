from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
  full_name: str
  email: str
  avatar: str | None

  class config:
    orm_mode: True


class CreateUserRequest(User):
  password: str


class CreateUserResponse(User):
  id: int


class Token(BaseModel):
  access_token: str
  token_type: str = "Bearer"
