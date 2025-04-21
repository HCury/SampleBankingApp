import pytest
import jwt
from datetime import datetime, timedelta
from routes.auth_routes import create_access_token

# filepath: c:\Users\Rick\Desktop\backend\routes\test_auth_routes.py

JWT_SECRET = "your_jwt_secret"
JWT_ALGORITHM = "HS256"

def test_create_access_token_success():
    data = {"sub": "testuser", "id": 1}
    token = create_access_token(data)
    assert token is not None

def test_create_access_token_contains_correct_data():
    data = {"sub": "testuser", "id": 1}
    token = create_access_token(data)
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert decoded_token["sub"] == "testuser"
    assert decoded_token["id"] == 1

def test_create_access_token_expiration():
    data = {"sub": "testuser", "id": 1}
    expires_delta = timedelta(seconds=1)
    token = create_access_token(data, expires_delta=expires_delta)
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert decoded_token["exp"] <= datetime.utcnow().timestamp() + 1