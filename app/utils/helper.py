import pytz
from datetime import datetime
from app.constant import constant
from passlib.context import CryptContext





class PasswordUtils():
    """This class is manage the password management"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str):
        """This function defines arguments that are used 
        for the hash password

        Arguments:
            password (str): Take pasword argument in string format

        Returns:
            Returns the hash of the password
        """
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        """This function defines arguments that are used 
        for the verify password

        Arguments:
            password (str): Take pasword argument in string format
            hashed_password(str): Take hash password argument in string format

        Returns:
            Returns the boolean value of the verify password
        """
        return self.pwd_context.verify(password, hashed_password)

def _get_datetime():
    return datetime.now(pytz.timezone('Asia/Kolkata')).replace(second=0, microsecond=0).replace(tzinfo=constant.STATUS_NULL)
