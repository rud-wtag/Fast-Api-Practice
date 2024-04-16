from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Cookie, HTTPException, status
from app.auth.interfaces import JWTTokenInterface
from app.auth.service import JWTTokenService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(
  access_token: str = Cookie(None),
  jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
):
  if access_token is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token"
    )
  user = jwt_token_service.verify_access_token(access_token)
  return user
