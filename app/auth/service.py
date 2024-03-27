from app.auth.interfaces import AuthInterface
from app.models.User import User
from app.auth.requests import CreateUserRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db


class AuthService(AuthInterface):
  def registration(
    self, create_user_request: CreateUserRequest, db: Session = Depends(get_db)
  ):
    user = User(
      ** create_user_request.dict()
    )
    db.add(user)
    db.commit()
    print(user)
    return user

  def login(self):
    """later"""
    pass

  def logout(self):
    """later"""
    pass
