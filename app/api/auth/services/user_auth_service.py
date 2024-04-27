from app.utils import helper
from app.utils import oauth2
from fastapi import status
from sqlalchemy.orm import Session
from app.constant import constant
from app.api.core import db_methods
from fastapi.encoders import jsonable_encoder
from app.api.auth.models.model import User
from app.api.core.db_methods import BaseMethod
from app.utils.message import InfoMessage, ErrorMessage
from app.utils.standard_response import StandardResponse


class UserAuthService:

    def user_signup_service(self, db: Session, body: dict):
        """
        Creates a new user account with the provided user data.
        Args:
            db (Session): The database session object.
            body (dict): The user data containing email and password.
        Returns:
            StandardResponse: The response object containing the status code, data, and message.
                - status code: HTTP_400_BAD_REQUEST if the email already exists or if there is an error.
                - data: The user data if the signup is successful.
                - message: The success message if the signup is successful, or the error message if there is an error.
        Raises:
            Exception: If there is an error during the signup process.
        """
        try:
            if user_object := BaseMethod(User).find_by_email(db, body.email):
                return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.emailAlreadyExist).make

            body.password = helper.PasswordUtils().hash_password(body.password)
            user_object = User(**body.dict())
            user_save = db_methods.BaseMethod(
                User).save(user_object, db)
            if not user_save:
                return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.genericError).make

            data = jsonable_encoder(user_object)
            return StandardResponse(status.HTTP_201_CREATED, data, InfoMessage.userCreated).make
        except Exception as e:
            return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.somethingWentWrong).make
        
    def user_login_service(self, db: Session, body: dict, Authorize):
        """
        Authenticates a user by checking their email and password.
        Args:
            db (Session): The database session object.
            body (dict): The user data containing email and password.
            Authorize: The authorization object.

        Returns:
            StandardResponse: The response object containing the status code, data, and message.
                - status code: HTTP_200_OK if the login is successful, HTTP_400_BAD_REQUEST if the email or password is invalid, 
                or HTTP_400_BAD_REQUEST if the user is not found.
                - message: The success message if the login is successful, or the error message if there is an error.
        Raises:
            Exception: If there is an error during the login process.
        """
        try:
            if user_object := BaseMethod(User).find_by_email(db, body.email):
                if helper.PasswordUtils().verify_password(body.password, user_object.password):    
                    token = oauth2.JWTOAuth2().token_generate(user_object.id, Authorize)
                    data = {
                        'access_token': token['access_token'],
                        'refresh_token': token['refresh_token']
                    }
                    return StandardResponse(status.HTTP_200_OK, data, InfoMessage.loggedInSuccessfully).make
                else:
                    return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.invalidPassword).make
            else:
                return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.userNotFound).make
        except Exception as e:
            return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.somethingWentWrong).make
