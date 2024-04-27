import json
from app.__init__ import app
from config import database
from fastapi.testclient import TestClient

client = TestClient(app)
getdb = database.get_db


class TestUserSignupService:
    
    def test_successful_signup(self):
        # Test successful user signup
        signup_data = {
            "email": "test2@example.com",
            "name": "testpassword",
            "password": "Test@123"
        }
        response = client.post("/v1/auth/user_signup/", json=signup_data)
        assert response.status_code == 201
        assert response.json()["message"] == "User created successfully"

    def test_signup_with_existing_email(self):
        # Test signup with existing email
        signup_data = {
            "email": "test1@example.com",  # Assuming this email already exists
            "password": "Test@123",
            "name": "john"
        }
        response = client.post("/v1/auth/user_signup/", json=signup_data)

        assert response.status_code == 400
        assert response.json()["message"] == "Email already exists"

    def test_signup_with_invalid_data(self):
        # Test signup with invalid data
        signup_data = {
            "email": "",  # Invalid email
            "password": "testpassword"
        }
        response = client.post("/v1/auth/user_signup/", json=signup_data)
        assert response.status_code == 422

    def test_error_handling(self):
        # Test error handling 
        invalid_data = {
            "email": "test@example.com",
            "password": "Test@123",
            "name": "john"
        }
        # Injecting an exception to force error handling
        app.dependency_overrides[getdb] = lambda: None  # Override dependency to return None
        response = client.post("/v1/auth/user_signup/", json=invalid_data)
        assert response.status_code == 400
        assert response.json()["message"] == "Woops, something's quite wrong, please try again!"

        # Remove the override
        del app.dependency_overrides[getdb]

class TestUserLoginService:
    def test_successful_login(self):
        # Test successful user login
        login_data = {
            "email": "johntest@gmail.com",
            "password": "Test@123"
        }
        response = client.post("/v1/auth/user_login/", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()['data']
        assert "refresh_token" in response.json()['data']

    def test_invalid_email_or_password(self):
        # Test login with invalid email or password
        login_data = {
            "email": "johntest@gmail.com",  # Assuming this email exists
            "password": "Tqst@123"
        }
        response = client.post("/v1/auth/user_login/", json=login_data)
        assert response.status_code == 400
        assert response.json()["message"] == " Password is invalid"

    def test_user_not_found(self):
        # Test login with non-existent user
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword"
        }
        response = client.post("/v1/auth/user_login/", json=login_data)
        assert response.status_code == 400
        assert response.json()["message"] == "User is not found"

    def test_error_handling(self):
        # Test error handling
        invalid_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        # Injecting an exception to force error handling
        app.dependency_overrides[getdb] = lambda: None  # Override dependency to return None
        response = client.post("/v1/auth/user_login/", json=invalid_data)
        assert response.status_code == 400
        assert response.json()["message"] == "Woops, something's quite wrong, please try again!"

        # Remove the override
        del app.dependency_overrides[getdb]

