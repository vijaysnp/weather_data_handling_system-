from config import jwt_config
from fastapi import Depends, Request
from fastapi_jwt_auth import AuthJWT


class JWTOAuth2:

    # @oauth2router.post('/token')
    def token_generate(self, uuid: str, Authorize: AuthJWT = Depends()):
        access_token = Authorize.create_access_token(subject=uuid,expires_time=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = Authorize.create_refresh_token(subject=uuid,expires_time=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"access_token": access_token, "refresh_token": refresh_token}