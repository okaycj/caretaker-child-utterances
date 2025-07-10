main: uv format type lint 

type:
	uv run mypy --strict .

lint:
	uv run ruff check --fix .
	uv run djlint --lint --quiet .

format:
	uv run ruff format .
	uv run djlint --reformat --quiet .
	uv run js-beautify -r ./static/**/*.js
	uv run css-beautify -r ./static/**/*.css

uv:
	uv self update
	uv sync

prod:
	uv sync --locked --no-default-groups
	uv run gunicorn --config gunicorn.conf.py wsgi:app

serve: main
	uv run flask run

deploy: main
	git push heroku main

train: main
	uv run python main.py