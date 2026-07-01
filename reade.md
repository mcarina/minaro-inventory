comando alembic
docker compose run --rm app alembic init -t async migrations
docker compose run --build --rm app alembic revision --autogenerate -m "create users roles user_roles tables"
docker compose run --rm app alembic upgrade head
