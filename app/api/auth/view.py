from fastapi import Depends, APIRouter
from pydantic import BaseModel
from config import jwt_config, database
from app.api.auth import schema
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from app.api.auth.services import user_auth_service 
                                

authrouter = APIRouter()
getdb = database.get_db


class Settings(BaseModel):

    authjwt_algorithm: str = jwt_config.JWT_ALGORITHM
    authjwt_secret_key: str = jwt_config.JWT_SECRET_KEY
    authjwt_access_token_expires: int = jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES


@AuthJWT.load_config
def get_config():
    return Settings()


class UserAuthentication():

    @authrouter.post("/user_signup")
    async def signup_user( body: schema.SigupClient,
                     db: Session = Depends(getdb)):
        response = user_auth_service.UserAuthService(
        ).user_signup_service(db, body)
        return response

    @authrouter.post("/user_login")
    async def login_user(body: schema.LoginUser,
                    db: Session = Depends(getdb),
                    Authorize: AuthJWT = Depends()):
        response = user_auth_service.UserAuthService(
        ).user_login_service(db, body, Authorize)
        return response

