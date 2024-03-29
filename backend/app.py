from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from compiler.evaluation import evaluation
from compiler.model import State

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/code")
async def code(json: dict):
    command = json["code"]
    response, message = evaluation(command)
    print(f"Result of command {command}: {response}")
    return {"response": response, "msg": message}


@app.get("/restart")
async def restart():
    State.restart()
    return {"response": {}, "msg": "ok"}
