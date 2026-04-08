import requests
import time
import os

# ✅ SAFE IMPORT (REQUIRED but no crash)
try:
    from openai import OpenAI
    client = OpenAI()
except Exception:
    client = None


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://mastanvali9381s-sre-env.hf.space"
)


def run_episode(level="easy"):
    print(f"\n=== START {level.upper()} ===")

    try:
        res = requests.post(f"{API_BASE_URL}/reset", params={"level": level})
        obs = res.json()
    except Exception as e:
        print("Reset failed:", e)
        return

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

        # FALLBACK
        if not action:
            action = {
                "type": "EXECUTE",
                "command": "ps"
            }

        print("STEP:", action)

        try:
            res = requests.post(f"{API_BASE_URL}/step", json=action)
            result = res.json()
        except Exception as e:
            print("Step failed:", e)
            break

        obs = result.get("observation", {})
        reward = float(result.get("reward", 0))
        done = result.get("done", False)

        print("RESULT:", reward, done)

        time.sleep(0.2)

    print(f"=== END {level.upper()} ===")


if __name__ == "__main__":
    try:
        run_episode("easy")
        run_episode("medium")
        run_episode("hard")
    except Exception as e:
        print("Fatal error:", e)