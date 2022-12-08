from time import perf_counter_ns

import numpy as np


# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minute(s)", "hour(s)", "day(s)"]
    idx = 0
    prev = 0
    while idx+1 < len(lengths) and time >= lengths[idx+1]:
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


def process_data(content):
    data = [list(map(int, line)) for line in content.split()]
    return np.array(data)


def check_data(data):
    pass
    # numpy will fail on non-rectangular data anyway
    # m = len(data[0])
    # for line in data:
    #     assert len(line) == m, "non rectangular data"


def task1(data):
    visible = np.zeros_like(data, dtype=bool)
    for d, v in [(data,          visible),
                 (data[:, ::-1], visible[:, ::-1]),
                 (data.T,        visible.T),
                 (data[::-1].T,  visible[::-1].T)]:
        for i in range(d.shape[0]):
            highest = -1
            for j in range(d.shape[1]):
                if d[i][j] > highest:
                    v[i][j] = True
                    highest = d[i][j]
                    if highest == 9:
                        # There are no higher trees
                        break
    return np.sum(visible)


def get_scenic_score(data, i0, j0):
    row = data[i0]
    column = data[:, j0]
    scores = [0, 0, 0, 0]
    for n, (start, dr, arr) in enumerate([
            (j0,  1, row),
            (j0, -1, row),
            (i0,  1, column),
            (i0, -1, column),
            ]):
        k = start + dr
        while 0 <= k and k < len(arr):
            if arr[k] < data[i0, j0]:
                scores[n] += 1
            else:
                break
            k += dr
        if 0 < k and k < len(arr)-1:
            scores[n] += 1
    return np.prod(scores)


def task2(data):
    score = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data[i])-1):
            score = max(score, get_scenic_score(data, i, j))
    return score


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
