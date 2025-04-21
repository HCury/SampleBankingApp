import pytest
from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from unittest.mock import MagicMock
from routes.transfer_routes import transfer_funds
from starlette.testclient import TestClient

# Create a custom test app without rate limiting middleware
test_app = FastAPI()

def get_current_user():
    return MagicMock()

def get_db():
    return MagicMock()

@test_app.post("/transfer")
def transfer_endpoint(request: Request, recipient_username: str, amount: float, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return transfer_funds(request, recipient_username, amount, current_user, db)

@pytest.fixture
def fake_request():
    client = TestClient(test_app)
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/transfer",
        "headers": [],
        "client": ("127.0.0.1", 12345),
    }
    return Request(scope)

def test_transfer_success(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"
    
    sender_account = MagicMock()
    sender_account.id = 1
    sender_account.balance = Decimal('100.00')

    recipient_user = MagicMock()
    recipient_user.id = 2
    recipient_user.username = "recipient"

    recipient_account = MagicMock()
    recipient_account.id = 2
    recipient_account.balance = Decimal('50.00')

    # Simulate .filter().first() calls in order
    db.query().filter().first.side_effect = [
        sender_account,        # sender_account
        recipient_user,        # recipient_user
        recipient_account      # recipient_account
    ]

    response = transfer_funds(fake_request, "recipient", 50.0, current_user, db)
    assert response == {"message": "Transfer successful"}

def test_transfer_invalid_amount(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.username = "sender"

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "recipient", -10.0, current_user, db)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Invalid amount"

def test_sender_account_not_found(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"

    db.query().filter().first.side_effect = [None]

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "recipient", 50.0, current_user, db)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Sender account not found"

def test_insufficient_funds(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"

    sender_account = MagicMock()
    sender_account.balance = Decimal('10.00')

    db.query().filter().first.side_effect = [sender_account]

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "recipient", 50.0, current_user, db)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Insufficient funds"

def test_recipient_not_found(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"

    sender_account = MagicMock()
    sender_account.balance = Decimal('100.00')

    db.query().filter().first.side_effect = [sender_account, None]

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "recipient", 50.0, current_user, db)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Recipient not found"

def test_recipient_account_not_found(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"

    sender_account = MagicMock()
    sender_account.balance = Decimal('100.00')

    recipient_user = MagicMock()
    recipient_user.id = 2
    recipient_user.username = "recipient"

    db.query().filter().first.side_effect = [sender_account, recipient_user, None]

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "recipient", 50.0, current_user, db)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Recipient account not found"

def test_self_transfer(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"

    sender_account = MagicMock()
    sender_account.balance = Decimal('100.00')

    recipient_user = MagicMock()
    recipient_user.id = 1  # Same as sender
    recipient_user.username = "sender"

    recipient_account = MagicMock()

    db.query().filter().first.side_effect = [sender_account, recipient_user, recipient_account]

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "sender", 50.0, current_user, db)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "You cannot transfer money to yourself."

def test_transfer_server_error(fake_request):
    db = MagicMock()
    current_user = MagicMock()
    current_user.id = 1
    current_user.username = "sender"

    sender_account = MagicMock()
    sender_account.id = 1
    sender_account.balance = Decimal('100.00')

    recipient_user = MagicMock()
    recipient_user.id = 2
    recipient_user.username = "recipient"

    recipient_account = MagicMock()
    recipient_account.id = 2
    recipient_account.balance = Decimal('50.00')

    db.query().filter().first.side_effect = [
        sender_account, recipient_user, recipient_account
    ]
    db.commit.side_effect = Exception("Simulated DB error")

    with pytest.raises(HTTPException) as excinfo:
        transfer_funds(fake_request, "recipient", 50.0, current_user, db)
    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Transfer failed due to server error"