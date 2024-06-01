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


# @pytest.fixture(scope="module")
# def start_server():
#     import subprocess
#     import time

#     process = subprocess.Popen(["uvicorn", "app.main:app", "--port", "8000"])
#     time.sleep(5)  # Give the server time to start
#     yield
#     process.terminate()


# @pytest.fixture(autouse=True)
# def change_test_dir(request, monkeypatch):
#     monkeypatch.chdir("chainlit_app")
