import random
from models import State, Observation


# ----------------------------
# Initialize Environment
# ----------------------------
def initialize_state(level="easy"):

    if level == "easy":
        bad_pid = random.randint(800, 1200)

        return State(
            system_status="failing",
            processes=[
                {"pid": 1, "name": "init"},
                {"pid": bad_pid, "name": "buggy_worker"}
            ],
            ports=[],
            logs=["High CPU usage detected"],
            files=[],
            budget_remaining=1.0,
            root_cause=f"process:{bad_pid}"
        )

    elif level == "medium":
        correct_port = 8080
        wrong_port = random.choice([8081, 9090])

        return State(
            system_status="failing",
            processes=[{"pid": 1, "name": "nginx"}],
            ports=[{"port": wrong_port}],
            logs=["Service not reachable on expected port"],
            files=["/etc/nginx.conf"],
            budget_remaining=1.0,
            root_cause=f"port:{correct_port}"
        )

    else:  # hard
        hidden_file = random.choice(
            ["/tmp/.hidden_cfg", "/tmp/.cache_file", "/tmp/.temp"]
        )

        return State(
            system_status="failing",
            processes=[{"pid": 1, "name": "web"}],
            ports=[],
            logs=[
                "Intermittent failures detected",
                "Possible config override"
            ],
            files=["/tmp/.hidden_cfg", "/tmp/.cache_file", "/tmp/.temp"],
            budget_remaining=1.0,
            root_cause=f"file:{hidden_file}"
        )


# ----------------------------
# Convert State → Observation
# ----------------------------
def get_observation(state: State, last_action=None):
    return Observation(
        system_status=state.system_status,
        processes=state.processes,
        ports=state.ports,
        logs=state.logs,
        files=state.files,
        budget_remaining=state.budget_remaining,
        last_action=last_action
    )


# ----------------------------
# Apply Action
# ----------------------------
def apply_action(state: State, action_type: str, command: str):

    reward = -0.05
    done = False

    # ----------------------------
    # EXECUTE
    # ----------------------------
    if action_type == "EXECUTE":
        if command == "ps":
            state.logs.append("Checked running processes")
            reward += 0.1

        elif command == "ls":
            state.logs.append("Listed files")
            reward += 0.1

        elif command == "netstat":
            state.logs.append("Checked ports")
            reward += 0.1

    # ----------------------------
    # APPLY PATCH
    # ----------------------------
    elif action_type == "APPLY_PATCH":

        # 🔥 SUPPORT: "kill 937"
        if command.lower().startswith("kill"):
            try:
                pid = int(command.split()[1])
            except:
                return state, -0.5, False

            # 🚨 service crash case
            if pid == 1:
                state.system_status = "crashed"
                state.logs.append("service_crashed")  # ✅ added
                reward = -1.0
                done = True
                return state, reward, done

            # remove process
            state.processes = [
                p for p in state.processes if p["pid"] != pid
            ]

            if f"process:{pid}" == state.root_cause:
                state.system_status = "healthy"
                reward += 1.0
                done = True
            else:
                reward -= 0.5

        # ORIGINAL FORMAT
        elif command.startswith("KILL_PROCESS"):
            pid = int(command.split(":")[1])

            if pid == 1:
                state.system_status = "crashed"
                state.logs.append("service_crashed")  # ✅ added
                reward = -1.0
                done = True
                return state, reward, done

            if f"process:{pid}" == state.root_cause:
                state.system_status = "healthy"
                reward += 1.0
                done = True
            else:
                reward -= 0.5

        # FIX PORT
        elif command.startswith("FIX_PORT"):
            if "port:8080" == state.root_cause:
                state.system_status = "healthy"
                reward += 1.0
                done = True
            else:
                reward -= 0.5

        # DELETE FILE
        elif command.startswith("DELETE_FILE"):
            file = command.split(":")[1]

            if f"file:{file}" == state.root_cause:
                state.system_status = "healthy"
                reward += 1.0
                done = True
            else:
                reward -= 0.5

    # ----------------------------
    # Budget
    # ----------------------------
    state.budget_remaining -= 0.05

    if state.budget_remaining <= 0:
        done = True

    return state, reward, done


print("NEW CODE RUNNING")