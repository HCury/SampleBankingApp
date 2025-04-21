# This file defines the registration routes for the FastAPI application. It includes the following key components:
# - Imports: Necessary libraries and modules, including FastAPI, SQLAlchemy, bcrypt, logging, and authentication dependencies.
# - Router: An instance of APIRouter to define the routes.
# - Logging: Configured using loguru to log information and errors to a JSON file.
# - Registration Route: A POST route /register that handles user registration.
# The route logs the request, checks if the username or email is already registered, hashes the password, creates a new user and account, updates the user count metric, and returns a success message.

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from sqlalchemy.orm import Session
import bcrypt
import time
from loguru import logger

from rate_limiter import limiter
from models import User, Account
from auth import get_db
from database import track_query, update_user_count

router = APIRouter()
logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="1 week", serialize=True)

@router.post("/register")
@limiter.limit("5 per minute")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    logger.info(f"User registration request | Username: {username} | Email: {email}")

    # Check if the username or email is already registered
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    track_query(start_time)

    if existing_user:
        logger.warning(f"Registration failed (Username or email already exists) | Username: {username} | Email: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    # Hash the password securely using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Create new user
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    track_query(start_time)

    logger.info(f"User registered successfully | User ID: {new_user.id} | Username: {username}")

    # Create an initial account with a default balance
    new_account = Account(user_id=new_user.id, balance=1000.00)
    db.add(new_account)
    db.commit()
    track_query(start_time)

    logger.info(f"Account created for user | User ID: {new_user.id} | Initial Balance: 1000.00")

    # Update user count metric
    update_user_count(db)

    return {"message": "Registration successful", "user_id": new_user.id}
