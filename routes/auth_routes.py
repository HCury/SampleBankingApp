# This file, defines the authentication routes for a FastAPI application. It includes the following key components:

# Imports: Necessary libraries and modules, including FastAPI, SQLAlchemy, JWT, bcrypt, Prometheus metrics, and logging.
# Router: An instance of APIRouter to define the routes.
# Logging: Configured using loguru to log information and errors to a JSON file.
# Prometheus Metrics: Counters and histograms to track login attempts, failed logins, successful logins, and login latency.
# JWT Token Generation: A function create_access_token to generate JWT tokens for authenticated users.
# Background Task: A function simulate_random_transaction to simulate random transactions for a user upon login.
# Login Route: A POST route /login that authenticates users, generates JWT tokens, logs login attempts, and adds a background task to simulate a random transaction.
# The file integrates rate limiting, logging, and metrics to provide a robust authentication mechanism for the application.

import bcrypt
import jwt
import os
import random
import time
from datetime import datetime, timedelta
from decimal import Decimal
from loguru import logger

from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User, Account, Transaction
from auth import get_db
from prometheus_client import Counter, Histogram

from database import SessionLocal, track_query
from rate_limiter import limiter

router = APIRouter()
# Configure logging
logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="1 week", serialize=True)

# Prometheus Metrics
LOGIN_ATTEMPTS = Counter("login_attempts", "Total login attempts")
FAILED_LOGINS = Counter("failed_logins", "Total failed login attempts")
SUCCESSFUL_LOGINS = Counter("successful_logins", "Total successful logins")
LOGIN_LATENCY = Histogram("login_latency_seconds", "Time taken for login process")

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """Generates a JWT token for authentication."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    logger.info(f"JWT token generated for user: {data['sub']}")
    return token


def simulate_random_transaction(user_id: int):
    start_time = time.time()
    db_session = SessionLocal()
    try:
        account = db_session.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            return

        transaction_type = random.choice(["deposit", "withdrawal"])
        amount = Decimal(str(round(random.uniform(10, 100), 2)))

        if transaction_type == "withdrawal" and account.balance < amount:
            transaction_type = "deposit"

        if transaction_type == "deposit":
            account.balance += amount
        else:
            account.balance -= amount

        txn = Transaction(
            account_id=account.id,
            transaction_type=transaction_type,
            amount=amount,
            description=f"Random {transaction_type} on login"
        )

        db_session.add(txn)
        db_session.commit()
        track_query(start_time)
        logger.info(f"[BG TASK] Simulated {transaction_type} of {amount} for user {user_id}")
    except Exception as e:
        logger.error(f"[BG TASK ERROR] {e}")
        db_session.rollback()
    finally:
        db_session.close()


@router.post("/login")
@limiter.limit("5/minute") 
def login(request: Request, background_tasks: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates the user, generates a token, and adds a random transaction."""
    LOGIN_ATTEMPTS.inc()
    start_time = time.time()

    logger.info(f"Login attempt | Username: {form_data.username} | IP: {request.client.host}")

    user = db.query(User).filter(User.username == form_data.username).first()
    track_query(start_time)
    
    if not user or not bcrypt.checkpw(form_data.password.encode("utf-8"), user.password_hash.encode("utf-8")):
        FAILED_LOGINS.inc()
        logger.warning(f"Failed login attempt | Username: {form_data.username} | Reason: Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    SUCCESSFUL_LOGINS.inc()
    token = create_access_token(data={"sub": user.username, "id": user.id})
    LOGIN_LATENCY.observe(time.time() - start_time)

    logger.info(f"Successful login | Username: {user.username}")

    background_tasks.add_task(simulate_random_transaction, user.id)
    
    return {"access_token": token, "token_type": "bearer"}
