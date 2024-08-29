import pytest
from app.config import get_session
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    session = get_session()
    yield session
    session.close()


@pytest.fixture(scope="module")
def test_client():
    yield client
