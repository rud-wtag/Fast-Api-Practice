import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.skip(reason="outdated tests")
def test_read_all_books(client, books):
  response = client.get("/books")
  assert response.status_code == 200
  assert isinstance(response.json(), list)
  assert response.json() == books


@pytest.mark.skip(reason="outdated tests")
def test_read_book(client, books):
  response = client.get(f"/books/Title%20One")
  assert response.json() == books[0]
  assert response.status_code == 200


@pytest.mark.skip(reason="outdated tests")
@pytest.mark.parametrize("category", ["science", "history"])
def test_read_category_by_query(client, category, books):
  response = client.get(f"/books/?category={category}")
  assert response.json() == [
    book for book in books if book["category"] == f"{category}"
  ]
  assert response.status_code == 200


@pytest.mark.skip(reason="outdated tests")
def test_create_book(client):
  new_book_data = {"title": "New Book", "author": "Author", "category": "Fiction"}
  response = client.post("/books/create_book", json=new_book_data)
  assert response.status_code == 200


# @pytest.mark.CRUD
# def test_update_book(client):
#     # Test update book functionality
#     pass

# @pytest.mark.CRUD
# def test_delete_book(client):
#     # Test delete book functionality
#     pass
