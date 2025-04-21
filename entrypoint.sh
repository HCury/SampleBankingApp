#!/bin/sh

set -e

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432 -U bank_user; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "PostgreSQL is ready. Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
