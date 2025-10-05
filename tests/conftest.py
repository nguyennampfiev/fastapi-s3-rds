import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    """Fixture to create a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c