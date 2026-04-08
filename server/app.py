from fastapi import FastAPI
import uvicorn
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


# 🔥 REQUIRED MAIN FUNCTION
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# 🔥 REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()