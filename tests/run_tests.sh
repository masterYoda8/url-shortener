#!/bin/bash

echo "Setting up the test database..."

docker run --name url-shortener-test-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test_db -p 5432:5433 -d postgres

echo "Waiting for the database to start..."
sleep 3

echo "Running tests..."
pytest

echo "Cleaning up the test database..."
docker stop url-shortener-test-db
docker rm url-shortener-test-db

echo "Tests finished."