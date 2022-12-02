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
    rounds = content.split("\n")
    return [r.split(" ") for r in rounds]


def score(player, computer):
    if player == computer:
        sc = 3 + computer
    elif player > computer:
        if player == 2 and computer == 0:
            sc = 6 + computer
        else:
            sc = computer
    else:
        if player == 0 and computer == 2:
            sc = computer
        else:
            sc = 6 + computer

    return sc + 1


def task1(data):
    result = 0
    ox = ord("X")
    oa = ord("A")
    for p, c in data:
        op, oc = ord(p) - oa, ord(c) - ox
        result += score(op, oc)

    return result


def task2(data):
    result = 0
    ox = ord("X")
    oa = ord("A")
    for p, c in data:
        op, oc = ord(p) - oa, ord(c) - ox
        if oc == 0:
            oc = op - 1
            if oc == -1: oc += 3
        elif oc == 1:
            oc = op
        else:
            oc = op + 1
            if oc == 3: oc -= 3

        result += score(op, oc)

    return result


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
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
