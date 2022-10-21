from fastapi import FastAPI

app = FastAPI()

STATE = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/code")
async def code(json: dict):
    STATE[json['key']] = eval(json['code'])
    return {"STATE": STATE}