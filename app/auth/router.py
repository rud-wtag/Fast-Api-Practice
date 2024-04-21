from fastapi import APIRouter, Depends, status, Cookie
from fastapi.responses import JSONResponse
from app.auth.schemas import CreateUserRequest, CreateUserResponse
from app.auth.interfaces import AuthInterface, JWTTokenInterface
from app.auth.service import AuthService, JWTTokenService
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.utils import get_current_user


auth_router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@auth_router.post(
  "/register", response_model=CreateUserResponse, status_code=status.HTTP_200_OK
)
async def register(
  create_user_request: CreateUserRequest,
  auth_service: AuthInterface = Depends(AuthService),
):
  user = auth_service.registration(create_user_request=create_user_request)
  return user


@auth_router.post("/login")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  auth_service: AuthInterface = Depends(AuthService),
):
  tokens = auth_service.login(form_data.username, form_data.password)
  response = JSONResponse(
    {"msg": "Logged in successfully", "access_token": tokens["access_token"]}
  )
  response.set_cookie(
    key="access_token", value=tokens["access_token"], httponly=True, secure=True
  )
  response.set_cookie(
    key="refresh_token", value=tokens["refresh_token"], httponly=True, secure=True
  )
  return response


@auth_router.post("/refresh_token")
async def refresh_token(
  jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
  refresh_token: str = Cookie(None),
):
  access_token = jwt_token_service.refresh_token(refresh_token)
  response = JSONResponse({"msg": "Token refreshed successfully"})
  response.set_cookie(
    key="access_token", value=access_token, httponly=True, secure=True
  )
  return response


@auth_router.post("/logout")
async def logout(
  user: dict = Depends(get_current_user),
  access_token=Cookie(None),
  refresh_token=Cookie(None),
  auth_service: AuthInterface = Depends(AuthService),
):
  return auth_service.logout(user, access_token, refresh_token)
