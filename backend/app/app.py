import traceback
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

STATE = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/code")
async def code(json: dict):
    response = ""
    try:
        command = json["code"]
        if "=" in command:
            command = command.split("=")
            evaluable = command[1]
            store = command[0].strip()
        else:
            evaluable = command
            store = "_"

        print("COMMAND", command)
        print("EVALUABLE", evaluable)
        response = eval(evaluable)
        STATE[store] = response
    except Exception:
        traceback.print_exc()
        response = "That didn't mean anything to me"
    finally:
        return {"STATE": STATE, "RESULT": response}
