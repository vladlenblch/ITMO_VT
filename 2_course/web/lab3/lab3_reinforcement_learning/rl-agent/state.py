from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class State:
    hits_last_10: int
    current_radius: float

    def discretize(self) -> Tuple[int, int]:
        return self.hits_last_10, int(self.current_radius)
