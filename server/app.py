from fastapi import FastAPI
from inference import reset, step, state

app = FastAPI()

@app.post("/reset")
def reset_api():
    return reset()

@app.post("/step")
def step_api(action: dict):
    return step(action)

@app.get("/state")
def state_api():
    return state()