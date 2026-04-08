import requests
import time

BASE_URL = "http://127.0.0.1:8000"


def run_episode(level="easy"):
    print(f"\n--- Running {level} task ---")

    # Reset environment
    res = requests.post(f"{BASE_URL}/reset", params={"level": level})
    obs = res.json()

    done = False
    steps = 0

    while not done and steps < 10:
        steps += 1

        action = None

        # EASY: detect buggy process
        for proc in obs.get("processes", []):
            if proc.get("name") == "buggy_worker":
                pid = proc.get("pid")
                action = {
                    "type": "APPLY_PATCH",
                    "command": f"KILL_PROCESS:{pid}"
                }
                break

        # MEDIUM: detect port issue
        if not action and obs.get("ports"):
            action = {
                "type": "APPLY_PATCH",
                "command": "FIX_PORT"
            }

        # HARD: detect hidden file
        if not action and obs.get("files"):
            for file in obs["files"]:
                if file.startswith("/tmp/."):
                    action = {
                        "type": "APPLY_PATCH",
                        "command": f"DELETE_FILE:{file}"
                    }
                    break

        # fallback
        if not action:
            action = {
                "type": "EXECUTE",
                "command": "ps"
            }

        print(f"Step {steps} → Action: {action}")

        # Send action to environment
        res = requests.post(f"{BASE_URL}/step", json=action)
        result = res.json()

        obs = result.get("obs", {})
        reward = result.get("reward", 0)
        done = result.get("done", False)

        print(f"Reward: {reward}, Done: {done}")

        time.sleep(1)

    print("Episode finished\n")


# Run all levels
if __name__ == "__main__":
    run_episode("easy")
    run_episode("medium")
    run_episode("hard")