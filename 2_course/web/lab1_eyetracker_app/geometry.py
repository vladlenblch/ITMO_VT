import time
from typing import Tuple


def check_point_in_area(x: float, y: float, r: float) -> Tuple[bool, float]:
    start_time = time.perf_counter_ns()

    if x < 0 < y:
        execution_time = time.perf_counter_ns() - start_time
        return False, execution_time

    if x > 0 and y > 0 and (x / r + y / (r / 2)) <= 1:
        execution_time = time.perf_counter_ns() - start_time
        return True, execution_time
    
    if x > 0 > y and (x * x + y * y) <= (r * r):
        execution_time = time.perf_counter_ns() - start_time
        return True, execution_time
    
    if x < 0 and y < 0 and (-r <= x <= 0) and (-r / 2 <= y <= 0):
        execution_time = time.perf_counter_ns() - start_time
        return True, execution_time
    
    execution_time = time.perf_counter_ns() - start_time
    return (x == 0 and -r / 2 <= y <= r) or (y == 0 and -r <= x <= r), execution_time
