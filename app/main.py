from fastapi import FastAPI
from app.api.v1.books import router
from app.auth.router import auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
  'http://localhost',
  'http://localhost:3000',
  'http://localhost:8080',
  'http://localhost:8000',
]

app.add_middleware(
  CORSMiddleware,
  allow_credentials=True,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router)