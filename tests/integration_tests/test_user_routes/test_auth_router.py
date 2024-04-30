from tests.conftest import USER
from app.auth.service import AuthService
from app.auth.interfaces import AuthInterface
from fastapi import Depends
from app.auth.schemas import CreateUserRequest


def test_create_user(client):
  data = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}

  response = client.post("/api/v1/register", json=data)
  assert response.status_code == 200
  assert "password" not in response.json()
  # assert data == response.json()


# def test_login(client, auth_service: AuthInterface = Depends(AuthService)):
#   create_user_request = CreateUserRequest(
#     full_name=USER["full_name"], email=USER["email"], password=USER["password"]
#   )
#   auth_service.registration(create_user_request)

#   response = client.post(
#     "/api/v1/login", json={"username": USER["email"], "password": USER["password"]}
#   )
#   assert response.status_code == 200
