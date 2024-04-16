from pydantic import BaseModel, Field, EmailStr, FilePath
from datetime import datetime
from fastapi import UploadFile


class User(BaseModel):
  role_id: int | None = Field(default=None)
  full_name: str
  email: EmailStr | None = Field(default=None)
  avatar: UploadFile

  class config:
    orm_mode: True


class CreateUserRequest(User):
  password: str = Field(min_length=8)

  model_config = {
    "json_schema_extra": {
      "examples": [
        {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}
      ]
    }
  }


class CreateUserResponse(User):
  id: int


class Token(BaseModel):
  id: int
  user_id: int
  access_token: str
  refresh_token: str
  status: bool
  # token_type: str = "Bearer"
  created_date: datetime
