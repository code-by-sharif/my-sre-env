from fastapi import FastAPI
from models import Action
from engine import initialize_state, get_observation, apply_action

app = FastAPI()

# Global state (simple version)
CURRENT_STATE = None


# ----------------------------
# RESET
# ----------------------------
@app.post("/reset")
def reset(level: str = "easy"):
    global CURRENT_STATE
    CURRENT_STATE = initialize_state(level)
    obs = get_observation(CURRENT_STATE)
    return obs


# ----------------------------
# STEP
# ----------------------------
@app.post("/step")
def step(action: Action):
    global CURRENT_STATE

    state, reward, done = apply_action(
        CURRENT_STATE,
        action.type,
        action.command
    )

    CURRENT_STATE = state
    obs = get_observation(state, last_action=action.command)

    return {
        "observation": obs,
        "reward": reward,
        "done": done
    }


# ----------------------------
# STATE (optional)
# ----------------------------
@app.get("/state")
def get_state():
    return CURRENT_STATE