from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.router import auth_router
from app.book.router import books_router
from app.core.middleware import PyinstrumentMiddleware, profile_middleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=profile_middleware)
# app.add_middleware(PyinstrumentMiddleware)

origins = [
  "http://localhost",
  "http://localhost:3000",
  "http://localhost:8080",
  "http://localhost:8000",
]

app.add_middleware(
  CORSMiddleware,
  allow_credentials=True,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(books_router)
