from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.auth.requests import CreateUserRequest, CreateUserResponse, Token
from app.auth.interfaces import AuthInterface
from app.auth.service import AuthService


auth_router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@auth_router.post("/register")
async def register(
  create_user_request: CreateUserRequest,
  db: Session = Depends(get_db),
  auth_service: AuthInterface = Depends(AuthService),
):
  user = auth_service.registration(create_user_request=create_user_request, db=db)
  res = CreateUserResponse(
    id=user.id, full_name=user.full_name, email=user.email, avatar=user.avatar
  )
  return JSONResponse(content={"User": res.dict()})


@auth_router.post("/login")
async def login(db: Session = Depends(get_db)):
  return ""
