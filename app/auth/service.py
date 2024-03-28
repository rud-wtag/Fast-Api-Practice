from app.auth.interfaces import AuthInterface
from app.models.User import User
from app.auth.schemas import CreateUserRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt
from app.core.config import settings

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/token')


class AuthService(AuthInterface):
  def __create__access_token(self, email: str, id: int, validity: timedelta):
    encode = {'sub': email, 'id': id}
    expires = datetime.now() + validity
    encode.update({'exp': expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

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
    token = self.__create__access_token(
      user.email,
      user.id,
      timedelta(minutes=20)
    )
    return token

  def logout(self):
    """later"""
    pass
