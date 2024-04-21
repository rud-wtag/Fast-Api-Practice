from typing import Annotated
from app.auth.interfaces import AuthInterface, JWTTokenInterface
from app.auth.models import User, Token, Role
from app.auth.schemas import CreateUserRequest
from fastapi import Depends, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.core.config import settings
from app.auth.constants import REFRESH_TOKEN, ACCESS_TOKEN, GUEST
from fastapi.responses import JSONResponse
from app.auth.constants import USER, GUEST, ADMIN
from fastapi_mail import FastMail, MessageSchema, MessageType
from starlette.background import BackgroundTasks

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTTokenService(JWTTokenInterface):
  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def store_token(self, user_id: int, token: str):
    token_model = Token(user_id=user_id, token=token)
    self.db.add(token_model)
    self.db.commit()
    return token_model

  def blacklist_token(self, user_id: int, token: str) -> bool:
    token_model = (
      self.db.query(Token)
      .filter(Token.user_id == user_id, Token.token == token)
      .first()
    )
    if token_model:
      token_model.status = False
      self.db.commit()
      self.db.refresh(token_model)
      return True
    return False

  def is_blacklist_token(self, user_id: int, token: str) -> bool:
    token_model = (
      self.db.query(Token)
      .filter(Token.user_id == user_id, Token.token == token)
      .first()
    )
    return token_model and not token_model.status

  def create_token(
    self, email: str, id: int, validity: timedelta, type: str = ACCESS_TOKEN
  ):
    encode = {"sub": email, "id": id, "type": type}
    expires = datetime.now() + validity
    encode.update({"exp": expires})
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    self.store_token(id, token)
    return token

  def verify_token(self, token: str):
    try:
      payload = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
      )
      username = payload.get("sub")
      user_id = payload.get("id")
      expire = payload.get("exp")
    except JWTError:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user",
      )

    if not username or not user_id:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the user",
      )

    expiration_time = datetime.fromtimestamp(expire)
    if expiration_time < datetime.now():
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
      )

    if self.is_blacklist_token(user_id, token):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token blacklisted",
      )

    user = (
      self.db.query(User)
      .filter(
        User.is_active == True,
        User.id == user_id,
      )
      .first()
    )

    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found or inactive",
      )

    return {"username": username, "id": user_id, 'role': user.role}

  def refresh_token(self, refresh_token: str) -> str | bool:
    token_details = self.verify_token(refresh_token)

    if token_details is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the user",
      )
    access_token = self.create_token(
      token_details["username"], token_details["id"], timedelta(minutes=20)
    )
    return access_token


class AuthService(AuthInterface):
  def __init__(
    self,
    db: Session = Depends(get_db),
    jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
  ):
    self.jwt_token_service = jwt_token_service
    self.db = db

  def save_role(self, user_role: str = GUEST):
    role = Role(name = user_role)
    self.db.add(role)
    self.db.commit()

  def registration(self, create_user_request: CreateUserRequest):
    role = self.db.query(Role).filter(Role.name == USER).first()
    print(role)
    user = User(
      **create_user_request.model_dump(exclude=["password", "role_id"]),
      password=bcrypt_context.hash(create_user_request.password),
      role_id = role.id
    )
    self.db.add(user)
    self.db.commit()
    return user
  
  # def create_reset_password_token(self, email: str):
  #   password_access_token = self.jwt_token_service.create_token(
  #     email, timedelta(minutes=20)
  #   )
  #   return password_access_token
  
  # def forgot_password(self, user, background_tasks: BackgroundTasks):
  #   try:
  #     password_access_token = self.jwt_token_service.create_token(
  #       user.email, timedelta(minutes=20)
  #     )
  #     forget_url_link =  f"{settings.APP_HOST}{settings.FORGET_PASSWORD_URL}/{password_access_token}"
      
  #     email_body = { "company_name": settings.MAIL_FROM_NAME,
  #                   "link_expiry_min": settings.FORGET_PASSWORD_LINK_EXPIRE_MINUTES,
  #                   "reset_link": forget_url_link }

  #     message = MessageSchema(
  #       subject="Password Reset Instructions",
  #       recipients=[user.email],
  #       template_body=email_body,
  #       subtype=MessageType.html
  #     )
      
  #     template_name = "mail/password_reset.html"

  #     fm = FastMail(mail_conf)
  #     background_tasks.add_task(fm.send_message, message, template_name)

  #     return JSONResponse(status_code=status.HTTP_200_OK,
  #       content={"message": "Email has been sent", "success": True,
  #           "status_code": status.HTTP_200_OK})
  #   except Exception as e:
  #     raise CustomHttpException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
  #           detail="Something Unexpected, Server Error", error_level=ErrorLevel.ERROR_LEVEL_2)


  def login(self, email: str, password: str):
    user = self.db.query(User).filter(User.email == email).first()

    if not user:
      return False
    if not bcrypt_context.verify(password, user.password):
      return False
    access_token = self.jwt_token_service.create_token(
      user.email, user.id, timedelta(minutes=20)
    )
    refresh_token = self.jwt_token_service.create_token(
      user.email, user.id, timedelta(days=7), type=REFRESH_TOKEN
    )
    return {"access_token": access_token, "refresh_token": refresh_token}

  def logout(self, user: dict, access_token: str, refresh_token: str):
    response = JSONResponse({"msg": "Logged out!"})
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    self.jwt_token_service.blacklist_token(user["id"], access_token)
    self.jwt_token_service.blacklist_token(user["id"], refresh_token)
    return response
