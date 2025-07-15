main: uv npm format type lint 

type:
	uv run mypy --strict .

lint:
	uv run ruff check --fix .
	uv run djlint --lint --quiet .
	npm run lint

format:
	uv run ruff format .
	uv run djlint --reformat --quiet .
	npm run format

uv:
	uv self update
	uv sync

npm:
	npm ci

prod:
	uv sync --locked --no-default-groups
	SECRET_KEY="production_secret_key" uv run gunicorn --config gunicorn.conf.py wsgi:app

serve: main
	npm run build
	uv run flask run --debug

deploy: main
	git push heroku main

train: main
	uv run python main.py