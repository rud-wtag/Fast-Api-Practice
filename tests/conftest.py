import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.api.v1.books import BOOKS


@pytest.fixture
def books():
  """Fixture for creating a FastAPI test client"""
  return BOOKS


@pytest.fixture
def client():
  """Fixture for creating a FastAPI test client"""
  return TestClient(app)


@pytest.fixture
def mock_db_connection(mocker):
  """Mock database connection"""
  with patch("app.DBConnection") as mock_db:
    mock_db_instance = mock_db.return_value
    yield mock_db_instance
