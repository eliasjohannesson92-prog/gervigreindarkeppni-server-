import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    """Test /health endpoint returns 200 + exact JSON"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    """Test /version endpoint returns 200 + required keys"""
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    
    # Check all required keys are present
    assert "status" in data
    assert "git_sha" in data
    assert "python_version" in data
    assert "challenge" in data
    
    # Verify basic types
    assert data["status"] == "ok"
    assert isinstance(data["python_version"], str)
    assert isinstance(data["challenge"], str)


def test_predict_happy_path():
    """Test /predict endpoint happy path returns 200"""
    response = client.post(
        "/predict",
        json={"inputs": {"text": "test data"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "outputs" in data


def test_predict_invalid_body():
    """Test /predict endpoint with invalid body returns 422"""
    # Missing required 'inputs' field
    response = client.post(
        "/predict",
        json={"invalid_field": "value"}
    )
    assert response.status_code == 422


def test_request_id_header():
    """Test that X-Request-ID header is generated or echoed"""
    # Test with custom request ID
    custom_id = "test-request-123"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.headers.get("X-Request-ID") == custom_id
    
    # Test without request ID - should generate one
    response = client.get("/health")
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0
