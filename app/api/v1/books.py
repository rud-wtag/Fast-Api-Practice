from fastapi import APIRouter, Body, Depends
from app.models.Book import Books
from app.core.database import get_db
from sqlalchemy.orm import Session


BOOKS = [
  {"title": "Title One", "author": "Author One", "category": "science"},
  {"title": "Title Two", "author": "Author Two", "category": "science"},
  {"title": "Title Three", "author": "Author Three", "category": "history"},
  {"title": "Title Four", "author": "Author Four", "category": "math"},
  {"title": "Title Five", "author": "Author Five", "category": "math"},
  {"title": "Title Six", "author": "Author Two", "category": "math"},
]

router = APIRouter(tags=["books"])


@router.get("/books")
async def read_all_books():
  return BOOKS


@router.get("/books/{book_title}")
async def read_book(book_title: str):
  for book in BOOKS:
    if book.get("title").casefold() == book_title.casefold():
      return book


@router.get("/books/")
async def read_category_by_query(category: str):
  books_to_return = []
  for book in BOOKS:
    if book.get("category").casefold() == category.casefold():
      books_to_return.append(book)
  return books_to_return


# Get all books from a specific author using path or query parameters
@router.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
  books_to_return = []
  for book in BOOKS:
    if book.get("author").casefold() == author.casefold():
      books_to_return.append(book)

  return books_to_return


@router.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
  books_to_return = []
  for book in BOOKS:
    if (
      book.get("author").casefold() == book_author.casefold()
      and book.get("category").casefold() == category.casefold()
    ):
      books_to_return.append(book)

  return books_to_return


@router.post("/books/create_book")
async def create_book(new_book=Body(None), db: Session = Depends(get_db)):
    print(new_book)
    book_model = Books()
    book_model.title = new_book['title']
    book_model.author = new_book['author']
    book_model.category = new_book['category']
    
    db.add(book_model)
    db.commit()
    
    return new_book


@router.put("/books/update_book")
async def update_book(updated_book=Body(None)):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@router.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
  for i in range(len(BOOKS)):
    if BOOKS[i].get("title").casefold() == book_title.casefold():
      BOOKS.pop(i)
      break
