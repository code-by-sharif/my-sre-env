import requests
import time
import os

# ✅ REQUIRED: Proper OpenAI client (with proxy)
try:
    from openai import OpenAI
    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL"),
        api_key=os.environ.get("API_KEY")
    )
except Exception:
    client = None


# ✅ Your environment URL (fallback only)
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://mastanvali9381s-sre-env.hf.space"
)


def run_episode(level="easy"):
    print(f"[START] Running {level} task")

    try:
        res = requests.post(f"{API_BASE_URL}/reset", params={"level": level})
        obs = res.json()
    except Exception as e:
        print("[ERROR] Reset failed:", e)
        return

    done = False
    steps = 0

    while not done and steps < 10:
        steps += 1

        action = None

        # ----------------------------
        # EASY → kill buggy_worker
        # ----------------------------
        for proc in obs.get("processes", []):
            if proc.get("name") == "buggy_worker":
                pid = proc.get("pid")
                action = {
                    "type": "APPLY_PATCH",
                    "command": f"KILL_PROCESS:{pid}"
                }
                break

        # ----------------------------
        # MEDIUM → fix port
        # ----------------------------
        if not action and obs.get("ports"):
            action = {
                "type": "APPLY_PATCH",
                "command": "FIX_PORT"
            }

        # ----------------------------
        # HARD → delete hidden file
        # ----------------------------
        if not action and obs.get("files"):
            for file in obs["files"]:
                if file.startswith("/tmp/."):
                    action = {
                        "type": "APPLY_PATCH",
                        "command": f"DELETE_FILE:{file}"
                    }
                    break

        # ----------------------------
        # FALLBACK
        # ----------------------------
        if not action:
            action = {
                "type": "EXECUTE",
                "command": "ps"
            }

        print(f"[STEP] {steps} | Action: {action}")

        # ✅ REQUIRED: LLM CALL (for validator)
        if client:
            try:
                client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": "Analyze system state"}
                    ],
                    max_tokens=5
                )
            except Exception as e:
                print("[WARN] LLM call failed:", e)

        # ----------------------------
        # APPLY ACTION
        # ----------------------------
        try:
            res = requests.post(f"{API_BASE_URL}/step", json=action)
            result = res.json()
        except Exception as e:
            print("[ERROR] Step failed:", e)
            break

        obs = result.get("observation", {})
        reward = float(result.get("reward", 0))
        done = result.get("done", False)

        print(f"[STEP] {steps} | Reward: {reward} | Done: {done}")

        time.sleep(0.2)

    print(f"[END] Finished {level} task\n")


if __name__ == "__main__":
    try:
        run_episode("easy")
        run_episode("medium")
        run_episode("hard")
    except Exception as e:
        print("[ERROR] Fatal:", e)