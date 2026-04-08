# 🚀 Ghost in the Machine: SRE Shadow-IT Investigator

## 🧠 Overview
This project implements a real-world OpenEnv environment simulating SRE (Site Reliability Engineering) incident response.

An AI agent must:
- investigate system state
- identify root cause
- apply correct fix

This project is designed as a reinforcement learning training environment for SRE decision-making.
This environment simulates real incident debugging workflows used by SRE engineers in production systems.

---

## 🎯 Objective
Restore the system to a healthy state with minimal steps and correct decisions.

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

## 🧪 Tasks

| Level  | Description |
|--------|------------|
| Easy   | Kill rogue process causing CPU spike |
| Medium | Fix service port mismatch |
| Hard   | Detect and remove hidden configuration file |

### Difficulty Scaling

- Easy → simple issue with clear signals  
- Medium → multiple signals with partial noise  
- Hard → hidden issues with misleading logs  

---

## 🎁 Reward Design

- +1.0 → correct fix  
- +0.1 → useful diagnostic actions  
- -0.05 → step penalty  
- -0.5 → incorrect action  
- -1.0 → critical failure  

### Reward Calculation Details

The reward is computed at each step based on system behavior:

- Correct fix immediately restores system → +1.0  
- Diagnostic actions that move towards solution → +0.1  
- Each step taken → -0.05 penalty (to encourage efficiency)  
- Wrong fix or irrelevant action → -0.5  
- Critical system failure or wrong major action → -1.0  

**Example:**
If the agent takes 5 steps and then applies the correct fix:  
Total reward = (5 × -0.05) + 1.0 = **+0.75**

---

## ⏱️ Episode Configuration

- Max Steps per Episode: 20  
- Episode ends when:
  - system is restored ✅  
  - or max steps reached ❌  

This ensures controlled training and evaluation.

---

## ⚠️ Error Handling

The environment returns structured errors for invalid or harmful actions:

- invalid_action  
- service_crashed  
- permission_denied  

---

## 🏋️ Training Support

This environment supports reinforcement learning algorithms such as:

- PPO (recommended)  
- DQN  
- A2C  

Agents interact using standard OpenEnv APIs: `step()`, `reset()`, `state()`.

### Example Training Loop

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

A simple rule-based agent is implemented in `inference.py`.

---

## ▶️ Run Locally

```bash
python -m uvicorn main:app --reload
```
