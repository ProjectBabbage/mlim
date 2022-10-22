launch:
	make front &
	make back

back:
	cd backend && poetry run uvicorn app.app:app --reload --port 8080

front:
	cd frontendts/ && npm run dev