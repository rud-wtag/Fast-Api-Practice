

def test_create_user(client):
  data = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}

  response = client.post('/api/v1/register', json=data)
  print(response)
  assert response.status_code == 200
  assert "password" not in response.json()
  assert data == response.json()