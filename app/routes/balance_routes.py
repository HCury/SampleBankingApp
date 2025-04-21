# This file defines the balance routes for the FastAPI application. It includes the following key components:
# - Imports: Necessary libraries and modules, including FastAPI, SQLAlchemy, logging, and authentication dependencies.
# - Router: An instance of APIRouter to define the routes.
# - Logging: Configured using loguru to log information and errors to a JSON file.
# - Balance Route: A GET route /balance that retrieves the balance for the authenticated user's account.
# The route logs the request, checks the user's account, tracks query execution time, and returns the account balance.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import time
from loguru import logger

from auth import get_current_user, get_db
from models import Account
from database import track_query

router = APIRouter()

# Configure logging
logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="1 week", serialize=True)

@router.get("/balance")
def get_balance(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    start_time = time.time()
    logger.info(f"Balance check request | User ID: {current_user.id}")

    account = db.query(Account).filter(Account.user_id == current_user.id).first()
    track_query(start_time)

    if not account:
        logger.warning(f"Balance check failed | User ID: {current_user.id} | Reason: Account not found")
        raise HTTPException(status_code=404, detail="Account not found")

    logger.info(f"Balance retrieved | User ID: {current_user.id} | Balance: {account.balance}")

    return {"balance": float(account.balance)}
