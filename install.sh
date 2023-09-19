#!/bin/bash

POSTGRES_DB="tgdb"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="123456"
DB_HOST="postgres_db"
DB_PORT=5432
DB_OUT_PORT=5434
SQLALCHEMY_LOG_LEVEL="CRITICAL"
TELEGRAM_TOKEN=""

echo "POSTGRES_DB=$POSTGRES_DB" > .env
echo "POSTGRES_USER=$POSTGRES_USER" >> .env
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env
echo "DB_HOST=$DB_HOST" >> .env
echo "DB_PORT=$DB_PORT" >> .env
echo "DB_OUT_PORT=$DB_OUT_PORT" >> .env
echo "SQLALCHEMY_LOG_LEVEL=$SQLALCHEMY_LOG_LEVEL" >> .env
echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" >> .env

docker compose up -d --build && \
docker exec -it tg_app alembic upgrade head