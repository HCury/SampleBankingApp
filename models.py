# This file defines the SQLAlchemy models for the FastAPI application. It includes the following key components:
# - User Model: Represents the users of the application with fields for id, username, email, and password hash.
# - Account Model: Represents the accounts associated with users, with fields for id, user_id, balance, and creation date.
# - Transaction Model: Represents the transactions associated with accounts, with fields for id, account_id, transaction type, amount, transaction date, and description.
# The models include necessary relationships, constraints, and indexes to ensure data integrity and efficient querying.


from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, Column, String, Index
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    __table_args__ = (
        Index('ix_user_username_email', 'username', 'email'),
    )


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    balance = Column(Numeric(15, 2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)