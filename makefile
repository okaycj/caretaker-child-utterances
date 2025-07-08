main: type lint format

type:
	uv run mypy --strict .

lint:
	uv run ruff check --fix .

format:
	uv run ruff format .

requirements:
	uv export --no-dev 

prod: main
	uv run gunicorn --config gunicorn.conf.py wsgi:app

serve: main
	uv run flask run
