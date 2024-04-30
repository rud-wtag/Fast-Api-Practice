from 
from tests.conftest import USER
from app.logger.logger import logger

def test_create_user(client):
  data = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}

  response = client.post("/api/v1/register", json=data)

  assert response.status_code == 200
  assert "password" not in response.json()


def test_login(client, insert_user_data):

  response = client.post(
    "/api/v1/login", data={"username": USER["email"], "password": USER["password"],'grant_type':None, 'scope':None, 'client_id':None,'client_secret':None}
  )

  assert response.status_code == 200
  assert response.cookies.get('access_token') is not None
  assert response.cookies.get('refresh_token') is not None


# def test_refresh_token(client):
#   response = client.post('/api/v1/login',cookies=Cookie())