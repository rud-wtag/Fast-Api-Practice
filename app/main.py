from fastapi import FastAPI
from app.api.v1.books import router
from app.auth.router import auth_router


app = FastAPI()

app.include_router(router)
app.include_router(auth_router)
