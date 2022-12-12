import heapq
from collections import deque
from time import perf_counter_ns
from typing import Deque, List, Tuple

from tqdm import tqdm


# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 0
    prev = 0
    while time > lengths[idx+1]:
        idx += 1
        time, prev = time//lengths[idx], time%lengths[idx]

    out = f"{time}{units[idx]}"
    if 0 < prev and time < 100:
        out += f" {prev}{units[idx-1]}"
    return out


def read_data(filename="input.txt"):
    with open(filename) as file:
        content = file.read().strip()

    return process_data(content)

# Ignore above


Pos = Tuple[int, int]
def process_data(content: str) -> Tuple[Pos, Pos, List[List[int]]]:
    start = None
    end = None
    lines = content.split("\n")
    height_map = [[0]*len(lines[0]) for _ in range(len(lines))]
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch == "S":
                start = (i, j)
                ch = "a"
            elif ch == "E":
                end = (i, j)
                ch = "z"

            if ch.isupper():
                height_map[i][j] = 26
            height_map[i][j] += ord(ch.lower()) - ord("a")
    assert start is not None
    assert end is not None
    return start, end, height_map


def check_data(data):
    pass


def task1(data):
    start, end, height_map = data
    n, m = len(height_map), len(height_map[0])
    visited = [[False]*m for _ in range(n)]
    # This might be called a heap, but it is actually a deque
    heap: Deque[Tuple[int, Pos]] = deque([(0, start)])
    while len(heap) > 0:
        dist, pos = heap.popleft()
        if pos == end:
            return dist
        i, j = pos
        if visited[i][j]:
            continue
        visited[i][j] = True
        for i2, j2 in [
                (i-1, j),
                (i+1, j),
                (i,   j-1),
                (i,   j+1),
                ]:
            if ((not (0 <= i2 < n and 0 <= j2 < m))
                    or height_map[i2][j2] > height_map[i][j] + 1
                    or visited[i2][j2]
                    ):
                continue
            heap.append((dist+1, (i2, j2)))
    raise ValueError("Did not find a way")


def task2(data):
    _, end, height_map = data
    n, m = len(height_map), len(height_map[0])
    visited = [[False]*m for _ in range(n)]
    # This might be called a heap, but it is actually a deque
    heap: Deque[Tuple[int, Pos]] = deque([(0, end)])
    while len(heap) > 0:
        dist, (i, j) = heap.popleft()
        if height_map[i][j] == 0:
            return dist
        if visited[i][j]:
            continue
        visited[i][j] = True
        for i2, j2 in [
                (i-1, j),
                (i+1, j),
                (i,   j-1),
                (i,   j+1),
                ]:
            if ((not (0 <= i2 < n and 0 <= j2 < m))
                    or height_map[i][j] > height_map[i2][j2] + 1
                    or visited[i2][j2]
                    ):
                continue
            heap.append((dist+1, (i2, j2)))
    raise ValueError("Did not find a way")


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
    check_data(data)
    t1 = perf_counter_ns()
    result1 = task1(data)
    t2 = perf_counter_ns()
    result2 = task2(data)
    t3 = perf_counter_ns()

    print(f"Data preprocessing in {format_ns(t1 - t0)}")
    print(f"Task 1: {result1} in {format_ns(t2 - t1)}")
    print(f"Task 2: {result2} in {format_ns(t3 - t2)}")


if __name__ == "__main__":
    main()
