from typing import Annotated
from app.auth.interfaces import AuthInterface, JWTTokenInterface
from app.models.User import User
from app.auth.schemas import CreateUserRequest
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.core.database import get_db
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.core.config import settings

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTTokenService(JWTTokenInterface):
  def create_access_token(self, email: str, id: int, validity: timedelta):
    encode = {"sub": email, "id": id}
    expires = datetime.now() + validity
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

  def verify_access_token(self, token: str):
    try:
      payload = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
      )
      username = payload.get("sub")
      user_id = payload.get("id")
      if username is None or user_id is None:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user"
        )
      return {"username": username, "id": user_id}
    except JWTError:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
      )


class AuthService(AuthInterface):
  def __init__(self, jwt_token_service: JWTTokenInterface = Depends(JWTTokenService)):
    self.jwt_token_service = jwt_token_service


  def registration(
    self, create_user_request: CreateUserRequest, db: Session = Depends(get_db)
  ):
    user = User(
      **create_user_request.model_dump(exclude=["password"]),
      password=bcrypt_context.hash(create_user_request.password),
    )
    db.add(user)
    db.commit()
    return user

  def login(self, email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
      return False
    if not bcrypt_context.verify(password, user.password):
      return False
    token = self.jwt_token_service.create_access_token(
      user.email, user.id, timedelta(minutes=20)
    )
    return token

  def logout(self):
    """later"""
    pass
