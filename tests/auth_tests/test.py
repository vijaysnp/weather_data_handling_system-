import sys
import os
from os.path import abspath, basename, dirname, join
from app.__init__ import app  
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from fastapi.encoders import jsonable_encoder
from app.api.auth.models.model import User 
from app.utils.message import InfoMessage, ErrorMessage
from app.api.auth.services.user_auth_service import user_signup_service
from app.utils.standard_response import StandardResponse
from app.api.core.db_methods import BaseMethod


# Helper function to mock database operations
def mock_db_operations(user_exists=False, save_success=True):
    user_mock = MagicMock() if user_exists else None
    find_by_email_mock = MagicMock(return_value=user_mock)
    save_mock = MagicMock(return_value=save_success)
    with patch.object(BaseMethod(User), "find_by_email", find_by_email_mock), \
         patch.object(BaseMethod(User), "save", save_mock):
        yield

class TestUserSignupService:

    def setup(self):
        self.app = app
        self.client = TestClient(self.app)

    def test_successful_signup(self):
        with mock_db_operations():
            data = {"email": "test@example.com", "password": "secret"}
            response = self.client.post("/v1/auth/user_signup", json=data)

            assert response.status_code == 201
            assert response.json() == {
                "status": "success",
                "data": jsonable_encoder(MagicMock(spec=User)),  # Mock user data
                "message": InfoMessage.userCreated
            }

    def test_existing_email(self):
        with mock_db_operations(user_exists=True):
            data = {"email": "test@example.com", "password": "secret"}
            response = self.client.post("/user_signup", json=data)

            assert response.status_code == 400
            assert response.json() == {
                "status": "error",
                "data": None,
                "message": ErrorMessage.emailAlreadyExist
            }

    def test_database_save_error(self):
        with mock_db_operations(save_success=False):
            data = {"email": "test@example.com", "password": "secret"}
            response = self.client.post("/user_signup", json=data)

            assert response.status_code == 400
            assert response.json() == {
                "status": "error",
                "data": None,
                "message": ErrorMessage.somethingWentWrong
            }

    def test_missing_email(self):
        data = {"password": "secret"}
        response = self.client.post("/user_signup", json=data)

        assert response.status_code == 422  # Unprocessable Entity (expected behavior)
        assert "email" in response.json()["detail"]  # Check for missing email error

    def test_missing_password(self):
        data = {"email": "test@example.com"}
        response = self.client.post("/user_signup", json=data)

        assert response.status_code == 422  # Unprocessable Entity (expected behavior)
        assert "password" in response.json()["detail"]  # Check for missing password error

if __name__ == "__main__":
    unittest.main()
