import random

class SREEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.load = random.randint(10, 50)
        self.failed = False
        self.step_count = 0
        print("\n[RESET] Environment initialized")
        return self.get_state()

    def get_state(self):
        return {
            "load": self.load,
            "failed": self.failed,
            "step": self.step_count
        }

    def step(self, action):
        self.step_count += 1

        # Apply action
        if action == "scale_up":
            self.load -= 10
        elif action == "scale_down":
            self.load += 5
        elif action == "restart":
            self.failed = False

        # Prevent negative load
        self.load = max(0, self.load)

        # Random failure (simulate real-world issue)
        if random.random() < 0.2:
            self.failed = True

        # Load fluctuation (dynamic system)
        self.load += random.randint(-5, 10)

        # Keep load within realistic range
        self.load = max(0, self.load)

        # ✅ LOGGING (SRE mindset)
        print(f"[LOG] Step {self.step_count} | Action: {action} | Load: {self.load} | Failed: {self.failed}")

        # Reward logic
        reward = 0

        if self.failed:
            reward -= 10  # heavy penalty for failure

        if 20 <= self.load <= 60:
            reward += 5  # optimal range
        elif self.load > 80:
            reward -= 5  # overload penalty
        else:
            reward += 1  # slight reward for stable low load

        return self.get_state(), reward