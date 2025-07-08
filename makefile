main: uv format type lint 

type:
	uv run mypy --strict .

lint:
	uv run ruff check --fix .
	uv run djlint --lint --quiet ./templates

format:
	uv run ruff format .
	uv run djlint --reformat --quiet ./templates

uv:
	uv self update
	uv sync

prod:
	uv sync --locked --no-default-groups
	uv run gunicorn --config gunicorn.conf.py wsgi:app

serve: main
	uv run flask run
