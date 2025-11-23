from dataclasses import dataclass
from typing import Tuple

from state import State

@dataclass(frozen=True)
class Action:
    label: str
    radius_delta: int

ACTIONS: Tuple[Action, ...] = (
    Action("increase_radius", 1),
    Action("decrease_radius", -1),
    Action("hold_radius", 0),
)

def compute_reward(state: State, action: Action) -> float:
    hits_ratio = state.hits_last_10 / 10

    if hits_ratio < 0.6:
        if action.radius_delta == 1:
            return 5.0
        if action.radius_delta == 0:
            return -1.0
        return -5.0

    if 0.6 <= hits_ratio <= 0.8:
        if action.radius_delta == 0:
            return 5.0
        return -1.0

    if hits_ratio > 0.8:
        if action.radius_delta == -1:
            return 5.0
        if action.radius_delta == 0:
            return -1.0
        return -5.0

    return 0.0
