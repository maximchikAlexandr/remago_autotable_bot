echo POSTGRES_DB=test_db > .env
echo POSTGRES_USER=postgres >> .env
echo POSTGRES_PASSWORD=123456 >> .env
echo DB_HOST=postgres_db >> .env
echo DB_PORT=5432 >> .env
echo DB_OUT_PORT=5434 >> .env
echo SQLALCHEMY_LOG_LEVEL=CRITICAL >> .env
echo TELEGRAM_TOKEN= >> .env

docker compose up -d --build && \
docker exec -it tg_app alembic upgrade head