# This file configures the rate limiter for the FastAPI application using SlowAPI.
# It includes the following key components:
# - Limiter: An instance of the Limiter class from SlowAPI.
# - Key Function: Uses get_remote_address to identify clients based on their IP address.

# rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
