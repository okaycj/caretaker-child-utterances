main: type lint format

type:
	uv run mypy --strict .

lint:
	uv run ruff check --fix .

format:
	uv run ruff format .

serve: main
	uv run flask run
