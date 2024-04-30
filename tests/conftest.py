import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock
from app.api.v1.books import BOOKS
from app.core.Base import Base
from app.core.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.core.config import settings


if settings.APP_ENV not in ["test"]:
  msg = f"ENV is not test, it is {settings.APP_ENV}"
  pytest.exit(msg)

engine = create_engine("sqlite:///./fastapi.db")
SessionTesting = sessionmaker(autoflush=False, autocommit=False, bind=engine)

USER = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}


@pytest.fixture
def books():
  """Fixture for creating a FastAPI test client"""
  return BOOKS


# @pytest.fixture
# USER = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}


@pytest.fixture
def test_session() -> Generator:
  """Test database connection"""
  db = SessionTesting()
  try:
    yield db
  finally:
    db.close()


@pytest.fixture(scope="function")
def app_test():
  Base.metadata.create_all(bind=engine)
  yield app
  Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app_test, test_session):
  """Fixture for creating a FastAPI test client"""

  def _test_db():
    try:
      yield test_session
    finally:
      pass

  app_test.dependency_overrides[get_db] = _test_db
  return TestClient(app_test)


@pytest.fixture
def mock_db_session():
  return MagicMock()


# @pytest.fixture
# def insert_user_data():
#   auth_service = AuthService()
#   create_user_request = CreateUserRequest(full_name=USER['full_name'], email=USER["email"], password=USER["password"])
#   auth_service.registration(create_user_request)
