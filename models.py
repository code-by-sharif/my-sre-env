from pydantic import BaseModel
from typing import List, Dict, Optional


# ----------------------------
# Observation Model
# ----------------------------
class Observation(BaseModel):
    system_status: str
    processes: List[Dict]
    ports: List[Dict]
    logs: List[str]
    files: List[str]
    budget_remaining: float
    last_action: Optional[str] = None


# ----------------------------
# Action Model
# ----------------------------
class Action(BaseModel):
    type: str   # EXECUTE / APPLY_PATCH / PROBE
    command: str


# ----------------------------
# State Model (internal)
# ----------------------------
class State(BaseModel):
    system_status: str
    processes: List[Dict]
    ports: List[Dict]
    logs: List[str]
    files: List[str]
    budget_remaining: float
    root_cause: str
    is_terminal: bool = False