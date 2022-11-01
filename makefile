install:
# python deps
	if ! [ -x "poetry -V" ]; then poetry install; else pip install -r requirements.txt; fi
# js deps
	cd frontend && npm i
	chmod +x mlim.sh
