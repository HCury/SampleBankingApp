import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.balance_routes import get_balance

# filepath: c:\Users\Rick\Desktop\backend\routes\test_balance_routes.py

def test_get_balance_success():
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    account = MagicMock()
    account.balance = 100.0

    db.query().filter().first.return_value = account

    response = get_balance(current_user, db)
    assert response == {"balance": 100.0}

def test_get_balance_account_not_found():
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1

    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_balance(current_user, db)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Account not found"