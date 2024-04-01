from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Cookie
from app.auth.interfaces import JWTTokenInterface
from app.auth.service import JWTTokenService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(
  token: str = Depends(oauth2_bearer),
  jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
):
  print('test==========',token)
  user = jwt_token_service.verify_access_token(token)
  return user
