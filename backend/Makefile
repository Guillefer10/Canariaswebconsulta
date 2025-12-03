.PHONY: init-db test lint

init-db:
	python -m app.db.init_db

upgrade:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "auto"

test:
	pytest

lint:
	python -m compileall app
