import time
import functools
from typing import Callable

__all__ = ["timeit", "load_lines"]


def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 0
    prev = 0
    while time > lengths[idx+1]:
        idx += 1
        time, prev = time // lengths[idx], time % lengths[idx]

    out = f"{time}{units[idx]}"
    if 0 < prev and time < 100:
        out += f" {prev}{units[idx-1]}"
    return out


def timeit(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        t0 = time.perf_counter_ns()
        out = func(*args, **kwargs)
        t1 = time.perf_counter_ns()
        print(f"Call {func.__name__} took {format_ns(t1 - t0)}")
        return out

    return inner_func


def load_lines(filename: str) -> list[str]:
    with open(filename) as file:
        out = file.read().strip().split("\n")
    return out
