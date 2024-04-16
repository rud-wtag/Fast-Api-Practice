from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import JSONResponse
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.auth.schemas import CreateUserRequest, CreateUserResponse, Token
from app.auth.interfaces import AuthInterface
from app.auth.service import AuthService
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.auth.utils import get_current_user


auth_router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@auth_router.post(
  "/register", response_model=CreateUserResponse, status_code=status.HTTP_200_OK
)
async def register(
  create_user_request: CreateUserRequest,
  db: Session = Depends(get_db),
  auth_service: AuthInterface = Depends(AuthService),
  # avatar: UploadFile = File(...)
):
  user = auth_service.registration(create_user_request=create_user_request, db=db)
  return user


@auth_router.post("/login")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db: Session = Depends(get_db),
  auth_service: AuthInterface = Depends(AuthService),
):
  token = auth_service.login(form_data.username, form_data.password, db=db)
  response = JSONResponse({"msg": "Logged in successfully"})
  response.set_cookie(key="access_token", value=token, httponly=True, secure=True)
  return response

@auth_router.post("/refresh")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db: Session = Depends(get_db),
  auth_service: AuthInterface = Depends(AuthService),
):
  token = auth_service.login(form_data.username, form_data.password, db=db)
  response = JSONResponse({"msg": "Logged in successfully"})
  response.set_cookie(key="access_token", value=token, httponly=True, secure=True)
  return response


@auth_router.post("/logout")
async def logout(
  user: dict = Depends(get_current_user),
):
  response = JSONResponse({"msg": "Logged out!"})
  response.delete_cookie(key="access_token")
  return response
