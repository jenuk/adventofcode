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
    data = []
    for line in content.split("\n"):
        first, second = line.split(",")
        a,b = first.split("-")
        c,d = second.split("-")
        a, b, c, d = map(int, (a, b, c, d))
        if c < a:
            a, b, c, d = c, d, a, b
        data.append([a, b, c, d])
    return data


def check_data(data):
    # process data will fail, if there is deviation from
    # the specified form instead
    pass


def task1(data):
    score = 0
    for a, b, c, d in data:
        score += d <= b or a == c
    return score


def task2(data):
    score = 0
    for a, b, c, d in data:
        score += c <= b
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
