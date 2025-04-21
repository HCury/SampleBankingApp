import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from main import app
from auth import get_db
from models import User, Account

client = TestClient(app)

# Override the get_db dependency with a mock session
@pytest.fixture
def mock_db():
    """Fixture to provide a fresh MagicMock for each test."""
    db = MagicMock(spec=Session)
    return db

def override_get_db():
    """Yield a MagicMock session for dependency injection."""
    db = MagicMock(spec=Session)
    yield db

app.dependency_overrides[get_db] = override_get_db


def test_register_success(mock_db):
    """
    Test that registration succeeds when the user does not exist.
    - Mocks the DB calls to simulate a user not found scenario.
    - Expects a 200 status and JSON response indicating success.
    """
    # Simulate 'no existing user' scenario
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Mock the add/commit/refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Mock the user ID upon insertion
    new_user = User(id=1, username="testuser", email="test@example.com", password_hash="hashedpassword")
    mock_db.refresh.side_effect = lambda obj: setattr(obj, "id", 1)  # Simulate DB refresh setting ID

    # Override the DB in the route
    app.dependency_overrides[get_db] = lambda: (yield mock_db)

    # Send the request
    response = client.post(
        "/register",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful", "user_id": 1}  # user_id should be 1

    # Verify DB calls
    mock_db.query.assert_called_once()  # or more specific checks
    mock_db.add.assert_called()         # user and account
    mock_db.commit.assert_called()


def test_register_existing_user(mock_db):
    """
    Test that registration fails when username or email already exists.
    - Mocks the DB calls to simulate an existing user scenario.
    - Expects a 400 status and JSON response indicating user already exists.
    """
    # Simulate 'existing user' scenario
    existing_user = User(id=1, username="testuser", email="test@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = existing_user

    # Override the DB in the route
    app.dependency_overrides[get_db] = lambda: (yield mock_db)

    # Send the request
    response = client.post(
        "/register",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    
    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Username or email already exists"}

    # Verify DB calls
    mock_db.query.assert_called_once()
    mock_db.add.assert_not_called()     # No user added
    mock_db.commit.assert_not_called()  # No commit if user already exists
