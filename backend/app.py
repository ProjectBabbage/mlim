import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from compiler.evaluation import evaluation

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
    response = ""
    try:
        command = json["code"]
        response = evaluation(command)
        print(f"Result of command {command}: {response}")
    except Exception:
        traceback.print_exc()
        response = "That didn't mean anything to me"
    finally:
        return {
            "RESULT": response,
        }
