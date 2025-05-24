#!/bin/sh
set -e

echo "Waiting for MySQL..."
until mysqladmin ping -h mysql -u root -ppassword --silent; do
  sleep 2
done

echo "Running ETL..."
python etl.py

echo "Bulk loading..."
python bulk_load.py

echo "Starting API server..."
uvicorn api:app --host 0.0.0.0 --port 8000