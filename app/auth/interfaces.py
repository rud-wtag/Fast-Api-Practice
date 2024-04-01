from abc import ABC, abstractmethod
from app.auth.schemas import CreateUserRequest
from sqlalchemy.orm import Session
from datetime import timedelta


class AuthInterface(ABC):
  """Auth interface to implement authentication"""

  @abstractmethod
  def registration(self, create_user_request: CreateUserRequest):
    """Registration function that will implement child class"""
    pass

  @abstractmethod
  def login(self, email: str, password: str, db: Session):
    """login function that will implement child class"""
    pass

  @abstractmethod
  def logout(self):
    """login function that will implement child class"""
    pass


class JWTTokenInterface(ABC):
  """Auth interface to implement authentication"""

  @abstractmethod
  def create_access_token(self, email: str, id: int, validity: timedelta):
    """Registration function that will implement child class"""
    pass

  @abstractmethod
  def verify_access_token(self, token: str):
    """login function that will implement child class"""
    pass
