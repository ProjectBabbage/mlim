launch:
	make front &
	make back

install:
# python deps
	if ! [ -x "$(command -v poetry)" ]; then poetry install; else pip install -r requirements.txt; fi
# js deps
	cd frontendts && npm i

back:
	if ! [ -x "$(command -v poetry)" ]; then cd backend && poetry run uvicorn app.app:app --reload --port 8080; else uvicorn app.app:app --reload --port 8080;fi

front:
	cd frontendts/ && npm run dev
