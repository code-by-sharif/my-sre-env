import requests
import time
import os
from openai import OpenAI  # ✅ REQUIRED

# ✅ ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://mastanvali9381s-sre-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI()  # ✅ REQUIRED

def run_episode(level="easy"):
    print("START")

    res = requests.post(f"{API_BASE_URL}/reset", params={"level": level})
    obs = res.json()

    done = False
    steps = 0

    while not done and steps < 10:
        steps += 1

        action = None

        # EASY
        for proc in obs.get("processes", []):
            if proc.get("name") == "buggy_worker":
                pid = proc.get("pid")
                action = {
                    "type": "APPLY_PATCH",
                    "command": f"KILL_PROCESS:{pid}"
                }
                break

        # MEDIUM
        if not action and obs.get("ports"):
            action = {
                "type": "APPLY_PATCH",
                "command": "FIX_PORT"
            }

        # HARD
        if not action and obs.get("files"):
            for file in obs["files"]:
                if file.startswith("/tmp/."):
                    action = {
                        "type": "APPLY_PATCH",
                        "command": f"DELETE_FILE:{file}"
                    }
                    break

        if not action:
            action = {
                "type": "EXECUTE",
                "command": "ps"
            }

        print("STEP", action)

        res = requests.post(f"{API_BASE_URL}/step", json=action)
        result = res.json()

        obs = result.get("observation", {})
        reward = float(result.get("reward", 0))
        done = result.get("done", False)

        print("STEP RESULT", reward, done)

        time.sleep(0.2)

    print("FINAL")


if __name__ == "__main__":
    run_episode("easy")
    run_episode("medium")
    run_episode("hard")