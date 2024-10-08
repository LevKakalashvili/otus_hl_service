test:
	@poetry run pytest

format_and_check_code:  # Для основного приложения
	poetry run isort app
	poetry run black app
	poetry run flake8 --config .flake8 app

format_and_check_code_test:  # Для тестов
	poetry run isort tests
	poetry run black tests
	poetry run flake8 --config .flake8 tests

format_and_check_code_all:  # Полная проверка
	make format_and_check_code
	make format_and_check_code_test

db_upgrade:
	poetry run alembic upgrade head

db_downgrade:
	poetry run alembic downgrade -1

db_create_migrate:
	poetry run alembic revision -m '$(name)' --autogenerate
