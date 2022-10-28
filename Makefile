launch:
	make front &
	make back

install:
# python deps
	if ! [ -x "$(command -v poetry)" ]; then poetry install; else pip install -r requirements.txt; fi
# js deps
	cd frontend && npm i

back:
	if ! [ -x "$(command -v poetry)" ]; then poetry run uvicorn backend.app:app --reload --port 8080; else uvicorn backend.app:app --reload --port 8080;fi

front:
	cd frontend/ && npm run dev


tests:
	python -m unittest discover
