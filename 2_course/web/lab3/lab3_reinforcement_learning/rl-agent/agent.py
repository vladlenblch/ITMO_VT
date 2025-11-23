import random
from collections import defaultdict
from typing import Dict, List, Tuple

from reward import ACTIONS, Action, compute_reward
from state import State

class RLAgent:
    def __init__(self) -> None:
        self.q_table: Dict[Tuple[int, int], List[float]] = defaultdict(
            lambda: [0.0 for _ in ACTIONS]
        )

    def select_action(self, state: State) -> Tuple[int, Action]:
        state_key = state.discretize()
        q_values = self.q_table[state_key]
        if random.random() < 0.1:
            idx = random.randrange(len(ACTIONS))
            return idx, ACTIONS[idx]
        max_q = max(q_values)
        best_indices = [i for i, q in enumerate(q_values) if q == max_q]
        idx = random.choice(best_indices)
        return idx, ACTIONS[idx]

    def update(self, state: State, action_index: int, reward: float, next_state: State) -> None:
        state_key = state.discretize()
        next_key = next_state.discretize()
        q_values = self.q_table[state_key]
        next_values = self.q_table[next_key]
        best_next = max(next_values)
        old = q_values[action_index]
        q_values[action_index] = old + 0.15 * (reward + 0.95 * best_next - old)

    def step(self, state: State, next_state: State, action_index: int) -> float:
        reward = compute_reward(state, ACTIONS[action_index])
        self.update(state, action_index, reward, next_state)
        return reward
