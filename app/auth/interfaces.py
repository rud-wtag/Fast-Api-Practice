from abc import ABC, abstractmethod
from app.auth.requests import CreateUserRequest


class AuthInterface(ABC):
  """Auth interface to implement authentication"""

  @abstractmethod
  def registration(self, create_user_request: CreateUserRequest):
    """Registration function that will implement child class"""
    pass

  @abstractmethod
  def login(self):
    """login function that will implement child class"""
    pass

  @abstractmethod
  def logout(self):
    """login function that will implement child class"""
    pass
