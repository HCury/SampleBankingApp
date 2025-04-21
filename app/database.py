# This file configures the database connection and ORM for the FastAPI application using SQLAlchemy.
# It includes the following key components:
# - Database URL: Configures the database connection URL, defaulting to a PostgreSQL database.
# - Engine: Creates a SQLAlchemy engine with connection pooling.
# - SessionLocal: Configures a sessionmaker for database sessions.
# - Base: Defines the declarative base for SQLAlchemy models.
# - Prometheus Metrics: Counters, histograms, and gauges to track database queries, execution time, and user count.
# - Utility Functions: Functions to update user count, track query execution time, and initialize the database schema.

import os
import sqlalchemy as sa

from time import time
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from prometheus_client import Counter, Histogram, Gauge

# Prometheus Metrics
DB_QUERY_COUNT = Counter("db_query_count", "Total number of database queries executed")
DB_QUERY_TIME = Histogram("db_query_time_seconds", "Time taken to execute database queries")
DB_QUERY_FAILURES = Counter("db_query_failures", "Total number of failed database queries")

# Use the Docker database service name (`db`) instead of localhost
# TODO: Change to your docker DB link if different
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bank_user:securepassword@db/banking_app")

engine = sa.create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

USER_COUNT = Gauge("user_count", "Total number of registered users")

def update_user_count(db: Session):
    """Update Prometheus gauge with the current user count."""
    from models import User
    user_count = db.query(User).count()
    USER_COUNT.set(user_count)

def track_query(start_time):
    """Manually increment the database query counter inside FastAPI routes."""
    query_time_ms = (time() - start_time) * 1000
    DB_QUERY_COUNT.inc()
    DB_QUERY_TIME.observe(query_time_ms)

def init_db():
    from models import Account, Transaction 
    Base.metadata.create_all(bind=engine)
