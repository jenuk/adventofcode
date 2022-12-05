from copy import deepcopy
from time import perf_counter_ns


# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 1
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
        content = file.read().rstrip()

    return process_data(content)

# Ignore above


def process_data(content):
    crates, moves = content.split("\n\n")
    crates = crates.split("\n")
    crates, last = crates[:-1], crates[-1]
    stacks, stack_pos = dict(), []
    for k, ch in enumerate(last):
        if ch == " ":
            continue
        stacks[ch] = []
        stack_pos.append((ch, k))
    for line in crates[::-1]:
        for ch, k in stack_pos:
            if k >= len(line) or line[k] == " ":
                continue
            stacks[ch].append(line[k])

    moves = moves.split("\n")
    moves = [m.split(" ") for m in moves]
    moves = [[int(m[1]), m[3], m[5]] for m in moves]

    return stacks, moves, stack_pos


def check_data(data):
    pass


def task1(data):
    crates, moves, stack_pos = data
    for k, start, stop in moves:
        crates[stop].extend(crates[start][-k:][::-1])
        crates[start] = crates[start][:-k]
    result = ""
    for ch, _ in stack_pos:
        result += crates[ch][-1]
    return result


def task2(data):
    crates, moves, stack_pos = data
    for k, start, stop in moves:
        crates[stop].extend(crates[start][-k:])
        crates[start] = crates[start][:-k]
    result = ""
    for ch, _ in stack_pos:
        result += crates[ch][-1]
    return result


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
    check_data(data)
    t1 = perf_counter_ns()
    result1 = task1(deepcopy(data))
    t2 = perf_counter_ns()
    result2 = task2(data)
    t3 = perf_counter_ns()

    print(f"Data preprocessing in {format_ns(t1 - t0)}")
    print(f"Task 1: {result1} in {format_ns(t2 - t1)}")
    print(f"Task 2: {result2} in {format_ns(t3 - t2)}")


if __name__ == "__main__":
    main()
