from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
  role_id: int | None = Field(default=None)
  full_name: str
  email: EmailStr | None = Field(default=None)
  # avatar: UploadFile | None

  class config:
    orm_mode: True


class CreateUserRequest(User):
  password: str = Field(min_length=6)

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
  user_id: int
  token: str
  status: bool = Field(default=True)
