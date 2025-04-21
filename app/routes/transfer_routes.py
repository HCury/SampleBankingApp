# This file defines the transfer routes for the FastAPI application. It includes the following key components:
# - Imports: Necessary libraries and modules, including FastAPI, SQLAlchemy, logging, and authentication dependencies.
# - Router: An instance of APIRouter to define the routes.
# - Prometheus Metrics: Counters and histograms to track money transferred, failed transfer attempts, and transfer latency.
# - Logging: Configured using loguru to log information and errors to a JSON file.
# - Transfer Route: A POST route /transfer that handles money transfers between user accounts.
# The route logs the request, validates the transfer details, updates account balances, creates transaction records, tracks query execution time, updates Prometheus metrics, and returns a success message.

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from decimal import Decimal
import time
from loguru import logger

from rate_limiter import limiter
from auth import get_current_user, get_db
from models import Account, Transaction, User
from database import track_query
from prometheus_client import Counter, Histogram

router = APIRouter()

# Prometheus Metrics
MONEY_TRANSFERRED = Counter("money_transferred", "Total amount of money transferred")
TRANSFER_FAILURES = Counter("transfer_failures", "Total failed transfer attempts")
TRANSFER_LATENCY = Histogram("transfer_latency_seconds", "Time taken for a transfer transaction")

logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="1 week", serialize=True)


@router.post("/transfer")
@limiter.limit("5 per minute")
def transfer_funds(
    request: Request,
    recipient_username: str,
    amount: float,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    start_time = time.time()  # Start tracking transaction latency

    logger.info(f"Transfer initiated | Sender: {current_user.username} | Recipient: {recipient_username} | Amount: {amount}")

    if amount <= 0:
        TRANSFER_FAILURES.inc()
        logger.warning(f"Transfer failed (Invalid amount) | Sender: {current_user.username} | Amount: {amount}")
        raise HTTPException(status_code=400, detail="Invalid amount")

    amount = Decimal(str(amount))

    sender_account = db.query(Account).filter(Account.user_id == current_user.id).first()
    if not sender_account:
        TRANSFER_FAILURES.inc()
        logger.error(f"Transfer failed (Sender account not found) | Sender: {current_user.username}")
        raise HTTPException(status_code=404, detail="Sender account not found")

    if sender_account.balance < amount:
        TRANSFER_FAILURES.inc()
        logger.warning(f"Transfer failed (Insufficient funds) | Sender: {current_user.username} | Balance: {sender_account.balance} | Amount: {amount}")
        raise HTTPException(status_code=400, detail="Insufficient funds")

    recipient_user = db.query(User).filter(User.username == recipient_username).first()
    if not recipient_user:
        TRANSFER_FAILURES.inc()
        logger.error(f"Transfer failed (Recipient not found) | Sender: {current_user.username} | Recipient: {recipient_username}")
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    recipient_account = db.query(Account).filter(Account.user_id == recipient_user.id).first()
    if not recipient_account:
        TRANSFER_FAILURES.inc()
        logger.error(f"Transfer failed (Recipient account not found) | Sender: {current_user.username} | Recipient: {recipient_username}")
        raise HTTPException(status_code=404, detail="Recipient account not found")
    
    if recipient_username == current_user.username:
        TRANSFER_FAILURES.inc()
        logger.warning(f"Transfer failed (Self-transfer) | Sender: {current_user.username}")
        raise HTTPException(status_code=400, detail="You cannot transfer money to yourself.")

    try:
        # Deduct from sender and add to recipient
        sender_account.balance = Decimal(str(sender_account.balance)) - amount
        recipient_account.balance = Decimal(str(recipient_account.balance)) + amount

        # Create transaction records
        txn_out = Transaction(
            account_id=sender_account.id,
            transaction_type="transfer",
            amount=amount,
            description=f"Transfer to {recipient_username}"
        )
        txn_in = Transaction(
            account_id=recipient_account.id,
            transaction_type="transfer",
            amount=amount,
            description=f"Transfer from {current_user.username}"
        )
        db.add(txn_out)
        db.add(txn_in)
        db.commit()

        # Track query execution time
        track_query(start_time)

        # Update Prometheus metrics
        MONEY_TRANSFERRED.inc(float(amount))
        TRANSFER_LATENCY.observe(time.time() - start_time)

        logger.info(f"Transfer successful | Sender: {current_user.username} | Recipient: {recipient_username} | Amount: {amount}")

        return {"message": "Transfer successful"}

    except Exception as e:
        TRANSFER_FAILURES.inc()
        db.rollback()

        logger.error(f"Transfer failed due to server error | Sender: {current_user.username} | Recipient: {recipient_username} | Amount: {amount} | Error: {str(e)}")
        
        raise HTTPException(status_code=500, detail="Transfer failed due to server error")
