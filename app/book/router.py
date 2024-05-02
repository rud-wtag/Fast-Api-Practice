from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.auth.utils import admin, auth
from app.book.models import Books
from app.core.database import get_db

books_router = APIRouter(prefix="/api/v1", tags=["books"], dependencies=[Depends(auth)])


@books_router.get("/books")
async def read_all_books(db: Session = Depends(get_db)):
  return db.query(Books).all()


@books_router.get("/books/title/{book_title}")
async def read_book_by_title(book_title: str, db: Session = Depends(get_db)):
  return db.query(Books).filter(Books.title == book_title).first()


@books_router.get("/books/category/{category}")
async def read_book_by_category(category: str, db: Session = Depends(get_db)):
  return db.query(Books).filter(Books.category == category).first()


@books_router.get("/books/author/{author}")
async def read_books_by_author(author: str, db: Session = Depends(get_db)):
  return db.query(Books).filter(Books.author == author).first()


@books_router.get("/books/author/{author}/category/{category}")
async def read_author_category_by_query(
  author: str, category: str, db: Session = Depends(get_db)
):
  return (
    db.query(Books).filter(Books.author == author, Books.category == category).first()
  )


@books_router.post("/books", dependencies=[Depends(admin)])
async def create_book(new_book=Body(None), db: Session = Depends(get_db)):
  book_model = Books()
  book_model.title = new_book["title"]
  book_model.author = new_book["author"]
  book_model.category = new_book["category"]

  db.add(book_model)
  db.commit()

  return new_book


@books_router.put("/books/{book_id}")
async def update_book(
  book_id: int, updated_book: dict = Body(None), db: Session = Depends(get_db)
):
  book = db.query(Books).filter(Books.id == book_id).first()
  try:
    if not book:
      raise HTTPException(status_code=404, detail="Book not found")
    for field, value in updated_book.items():
      setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book
  except HTTPException as e:
    return e
  except Exception as e:
    return e


@books_router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
  book = db.query(Books).filter(Books.id == book_id).first()
  try:
    if not book:
      raise HTTPException(status_code=404, detail="Book not found")
    book = db.delete(book)
    db.commit()
    return JSONResponse(content="books deleted successfully")
  except HTTPException as e:
    return e
  except Exception as e:
    return e
