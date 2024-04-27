import pytest
from app.__init__ import app
from fastapi.testclient import TestClient

client = TestClient(app)

mock_token = "mock_token"
class TestWeatherdataService:

    def test_valid_request(self):
        latitude = 40.7128
        longitude = 15.25
        days = 1
        headers = {"Authorization": f"Bearer {mock_token}"}
        response = client.get(f"/v1/historic-weather/data?latitude={latitude}&longitude={longitude}&days={days}", headers=headers)
        assert response.status_code == 200
        assert "data" in response.json()
       
    def test_missing_parameters(self):
        headers = {"Authorization": f"Bearer {mock_token}"}
        response = client.get("/v1/historic-weather/data", headers=headers)
        assert response.status_code == 422  # FastAPI returns 422 for validation errors

    def test_invalid_token(self):
        response = client.get("/v1/historic-weather/data?latitude=40.7128&longitude=-74.0060&days=1")
        assert response.status_code == 403

    def test_invalid_coordinates(self):
        headers = {"Authorization": f"Bearer {mock_token}"}
        response = client.get("/v1/historic-weather/data?latitude=91&longitude=181&days=1", headers=headers)
        assert response.status_code == 400

