from time import perf_counter_ns
from typing import List, Tuple


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


def process_data(content: str) -> List[Tuple[str, int]]:
    data = [((a := line.split(" "))[0], int(a[1]))
            for line in content.split("\n")]
    # this would require one less loop later, but unnecessary amounts
    # of memory usage
    # data = [d for d, c in data for _ in range(c)]
    return data


def check_data(data):
    pass


def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1


def snakey(data: List[Tuple[str, int]], n: int) -> int:
    # my editor is annoying without this typing hint
    snake: List[Tuple[int, int]] = [(0, 0) for _ in range(n)]
    visited = {snake[0]}
    d_to_dx = {
        "U": ( 0,  1),
        "D": ( 0, -1),
        "R": ( 1,  0),
        "L": (-1,  0),
    }
    for d, c in data:
        for _ in range(c):
            dx, dy = d_to_dx[d]
            snake[0] = (snake[0][0]+dx,snake[0][1]+dy)
            for k in range(1, len(snake)):
                dx, dy = snake[k-1][0] - snake[k][0], snake[k-1][1] - snake[k][1]
                if abs(dx) >= 2 or abs(dy) >= 2:
                    snake[k] = (snake[k][0]+sign(dx), snake[k][1]+sign(dy))
            visited.add(snake[-1])
    return len(visited)


def task1(data: List[Tuple[str, int]]) -> int:
    return snakey(data, 2)


def task2(data: List[Tuple[str, int]]) -> int:
    return snakey(data, 10)


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
