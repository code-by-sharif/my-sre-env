---
title: SRE Environment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
python_version: "3.10"
app_port: 7860
---

# 🚀 Ghost in the Machine: SRE Shadow-IT Investigator

## 🧠 Overview
This project implements a real-world OpenEnv environment simulating SRE (Site Reliability Engineering) incident response.

An AI agent interacts with the system to:
- investigate system state  
- identify root cause  
- apply the correct fix  

This environment is designed for training and evaluating decision-making agents in realistic debugging scenarios.

---

## 🌍 Real-World Relevance
This environment models real production issues commonly handled by SRE engineers:

- Rogue processes causing high CPU usage  
- Incorrect service configurations (ports)  
- Hidden configuration overrides  

Such environments can be used to train autonomous agents for:
- system monitoring  
- automated debugging  
- self-healing infrastructure  

---

## 🎯 Objective
Restore the system to a healthy state using correct decisions in minimal steps.

---

## 🧱 Environment Design

### Observation Space
- system_status  
- processes  
- ports  
- logs  
- files  
- budget_remaining  

### Action Space
- EXECUTE (ps, ls, netstat)  
- APPLY_PATCH (kill process, fix port, delete file)

---

## 🔄 Environment Workflow
```text
reset → observation → decision → step → repeat → done
```

---

## 🧪 Tasks

| Level  | Description |
|--------|------------|
| Easy   | Kill rogue process causing CPU spike |
| Medium | Fix service port mismatch |
| Hard   | Detect and remove hidden configuration file |

### Difficulty Scaling
- Easy → clear and direct signal  
- Medium → partial ambiguity  
- Hard → hidden root cause with multiple possibilities  

---

## 🎁 Reward Design

- +0.95 → correct fix (task completed)  
- +0.1 → intermediate or incorrect action  

### Reward Behavior
- High reward when correct root cause is fixed  
- All other actions return small positive reward  
- Rewards strictly remain in range (0, 1)  

Example:  
If the agent takes 3 steps and then fixes correctly:  
Total reward = (3 × 0.1) + 0.95 = 1.25  

---

## ⏱️ Episode Configuration
- Max Steps per Episode: 20  
- Episode ends when:
  - system is restored  
  - or max steps reached  

---

## ⚠️ Error Handling
- invalid_action  
- service_crashed  
- permission_denied  

---

## 🧠 Design Decisions
- Rule-based baseline agent ensures deterministic behavior  
- Progressive difficulty simulates real-world debugging  
- Reward structure ensures stable evaluation  
- Trial-based elimination used in hard level  

---

## 🏋️ Training Support
Supports:
- PPO  
- DQN  
- A2C  

Example loop:

```python
state = env.reset()

for step in range(20):
    action = agent.choose_action(state)
    state, reward, done, _ = env.step(action)

    if done:
        break
```

---

## 🤖 Baseline Agent
Implemented in inference.py:
- analyzes observation  
- selects action  
- solves tasks  

---

## ▶️ Run Locally
```bash
python -m uvicorn main:app --reload
```

---

## 🏆 Key Strengths
- Real-world SRE simulation  
- Clean environment design  
- Stable reward system  
- Clear action-observation mapping  
- OpenEnv compliant  

---

## 🚀 Future Scope
Can be extended into real-world self-healing systems where agents automatically detect and fix production issues.