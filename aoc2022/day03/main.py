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
        content = file.read().strip()

    return process_data(content)

# Ignore above


def process_data(content):
    backpacks = content.split("\n")
    for k, line in enumerate(backpacks):
        m = len(line) // 2
        a, b = line[:m], line[m:]
        assert len(a) == len(b)
        backpacks[k] = [set(a), set(b)]
    return backpacks


def check_data(data):
    letters = {chr(ord("A")+k) for k in range(26)}
    letters = letters | {chr(ord("a")+k) for k in range(26)}
    assert len(data)%3 == 0
    for a, b in data:
        assert set(a) <= letters
        assert set(b) <= letters


def score(item: str) -> int:
    res = 0
    if ord(item) < ord("a"):
        res += 26
        item = item.lower()
    res += ord(item) - ord("a") + 1
    return res


def task1(data):
    res = 0
    for a, b in data:
        inter = a & b
        assert len(inter) == 1
        item = next(iter(inter))
        res += score(item)

    return res


def task2(data):
    res = 0
    for k in range(0, len(data), 3):
        group = data[k:k+3]
        group = [a | b for a, b in group]
        inter = set.intersection(*group)
        assert len(inter) == 1
        item = next(iter(inter))
        res += score(item)

    return res


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
