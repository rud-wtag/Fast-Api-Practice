from app.auth.service import AuthService
from app.auth.models import Role, Token
from app.auth.models import User
from app.core.config import settings
import pytest
from unittest.mock import MagicMock, patch
from jose import jwt
from datetime import datetime, timedelta
from freezegun import freeze_time
from fastapi import HTTPException
from app.auth.constants import GUEST

class TestAuthService:
  def setup_method(self):
    self.user = {"role": 'admin', "token": "test_token"}

  def test_save_role(self, mock_db_session):
    auth_service = AuthService(db=mock_db_session)

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    result = auth_service.save_role(self.user.get("role"))

    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    assert result == None
    actual_role_arg = mock_db_session.add.call_args.args[0]
    print("Role object passed to add method:", actual_role_arg)  # Debugging
    # mock_db_session.add.assert_called_once_with(Role(name=self.user.get("role")))
    mock_db_session.add.assert_called_once_with(Role(name=self.user.get("role")))
    # assert mock_db_session.add.call_args[0][0] == Role(name = GUEST)
    # assert mock_db_session.add.call_args_list[0][0] == (
    #   Role(name='guest')
    # )