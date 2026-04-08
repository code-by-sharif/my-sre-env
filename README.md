# 🚀 Ghost in the Machine: SRE Shadow-IT Investigator

## 🧠 Overview
This project implements a real-world OpenEnv environment simulating SRE (Site Reliability Engineering) incident response.

An AI agent must:
- investigate system state
- identify root cause
- apply correct fix

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

---

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

---

## 🎁 Reward Design

- +1.0 → correct fix  
- +0.1 → useful diagnostic actions  
- -0.05 → step penalty  
- -0.5 → incorrect action  
- -1.0 → critical failure  

---

## 🤖 Baseline Agent

A simple agent is implemented in `inference.py`.

---

## ▶️ Run Locally

```bash
python -m uvicorn main:app --reload