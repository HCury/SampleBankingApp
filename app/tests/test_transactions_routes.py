# tests/test_transactions_routes.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime
from decimal import Decimal

from main import app
from auth import get_db, get_current_user
from models import Account, Transaction

client = TestClient(app)

def override_get_db():
    """Provide a MagicMock session instead of a real DB."""
    db = MagicMock()
    yield db
    db.close()

def override_get_current_user():
    """Simulate a logged-in user with ID=123."""
    mock_user = MagicMock()
    mock_user.id = 123
    return mock_user

# Apply the overrides to all tests in this file
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_transactions_no_account():
    """
    If the user has no account, /transactions should return 404 with "Account not found".
    """
    mock_db = MagicMock()
    # When we query for the account, return None to simulate "no account"
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Override get_db for this test
    app.dependency_overrides[get_db] = lambda: (yield mock_db)

    # Make the GET request
    response = client.get("/transactions")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found"}

    # Clean up
    app.dependency_overrides[get_db] = override_get_db


def test_get_transactions_success():
    """
    If the user has an account, /transactions should return a list of transaction data.
    """
    mock_db = MagicMock()

    # 1️⃣ Mock the Account
    mock_account = Account(id=1, user_id=123, balance=Decimal("1000.00"))
    mock_db.query.return_value.filter.return_value.first.return_value = mock_account

    # 2️⃣ Mock some Transactions
    mock_tx1 = Transaction(
        id=10,
        account_id=1,
        transaction_type="deposit",
        amount=Decimal("50.00"),
        transaction_date=datetime(2025, 1, 1, 12, 0),
        description="Mock deposit"
    )
    mock_tx2 = Transaction(
        id=11,
        account_id=1,
        transaction_type="withdrawal",
        amount=Decimal("20.00"),
        transaction_date=datetime(2025, 1, 2, 13, 0),
        description="Mock withdrawal"
    )

    # 3️⃣ Mock the query chain to return these transactions
    mock_db.query.return_value.filter.return_value.order_by.return_value\
          .offset.return_value.limit.return_value.all.return_value = [mock_tx1, mock_tx2]

    # Override get_db for this test
    app.dependency_overrides[get_db] = lambda: (yield mock_db)

    # Make the GET request (with pagination params, if desired)
    response = client.get("/transactions?page=1&limit=10")

    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert len(data["transactions"]) == 2

    # 4️⃣ Validate the first transaction
    assert data["transactions"][0]["id"] == 10
    assert data["transactions"][0]["transaction_type"] == "deposit"
    assert data["transactions"][0]["amount"] == 50.0
    assert data["transactions"][0]["description"] == "Mock deposit"

    # 5️⃣ Validate the second transaction
    assert data["transactions"][1]["id"] == 11
    assert data["transactions"][1]["transaction_type"] == "withdrawal"
    assert data["transactions"][1]["amount"] == 20.0
    assert data["transactions"][1]["description"] == "Mock withdrawal"

    # Clean up
    app.dependency_overrides[get_db] = override_get_db
