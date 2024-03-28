from pydantic import BaseModel


class CreateUserRequest(BaseModel):
  full_name: str
  email: str
  password: str
  avatar: str | None


class CreateUserResponse(BaseModel):
  id: int
  full_name: str
  email: str
  avatar: str | None


class Token(BaseModel):
  access_token: str
  token_type: str
