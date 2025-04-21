# This file defines the transaction routes for the FastAPI application. It includes the following key components:
# - Imports: Necessary libraries and modules, including FastAPI, SQLAlchemy, logging, and authentication dependencies.
# - Router: An instance of APIRouter to define the routes.
# - Logging: Configured using loguru to log information and errors to a JSON file.
# - Transactions Route: A GET route /transactions that retrieves the transactions for the authenticated user's account.
# The route logs the request, checks the user's account, tracks query execution time, and returns the transactions.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from loguru import logger

from auth import get_current_user, get_db
from models import Account, Transaction
from database import track_query

router = APIRouter()

# Configure logging
logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="1 week", serialize=True)

@router.get("/transactions")
def get_transactions(page: int = 1, limit: int = 10, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    start_time = time.time()

    logger.info(f"Fetching transactions | User: {current_user.username} | Page: {page} | Limit: {limit}")

    offset = (page - 1) * limit
    account = db.query(Account).filter(Account.user_id == current_user.id).first()
    track_query(start_time)

    if not account:
        logger.warning(f"Transactions fetch failed (Account not found) | User: {current_user.username}")
        raise HTTPException(status_code=404, detail="Account not found")

    txns = (
        db.query(Transaction)
        .filter(Transaction.account_id == account.id)
        .order_by(Transaction.transaction_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    transactions = [
        {
            "id": txn.id,
            "transaction_type": txn.transaction_type,
            "amount": float(txn.amount),
            "transaction_date": txn.transaction_date,
            "description": txn.description,
        }
        for txn in txns
    ]

    logger.info(f"Transactions retrieved | User: {current_user.username} | Transactions: {len(transactions)}")

    return {"transactions": transactions}
