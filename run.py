from env import SREEnvironment
import random

env = SREEnvironment()
state = env.reset()

print("Initial State:", state)

for i in range(10):
    action = random.choice(["scale_up", "scale_down", "restart"])
    state, reward = env.step(action)

    print("\nStep:", i+1)
    print("Action:", action)
    print("State:", state)
    print("Reward:", reward)