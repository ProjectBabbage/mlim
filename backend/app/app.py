import traceback
from evaluation import evaluation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = {}  # state of the python kernel
CELLS = []  # latex code of each cells


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/code")
async def code(json: dict):
    response = ""
    try:
        command = json["code"]
        response = evaluation(STATE, command)
        print(f"Result of command {command}: {response}")
    except Exception:
        traceback.print_exc()
        response = "That didn't mean anything to me"
    finally:
        return {"STATE": STATE, "CELLS": CELLS, "RESULT": response}
