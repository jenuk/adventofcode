from time import perf_counter_ns


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


def process_data(content):
    data = content.split("\n")
    for k in range(len(data)):
        if data[k][0] == "a":
            data[k] = int(data[k].split(" ")[1])
        else:
            data[k] = None
    return data


def check_data(data):
    pass


def cycle_iterate(data):
    cyc = 1
    for el in data:
        if el is None:
            yield cyc, 0
        else:
            yield cyc, 0
            cyc += 1
            yield cyc, el
        cyc += 1


def task1(data):
    score = 0
    reg = 1
    for cyc, el in cycle_iterate(data):
        if cyc % 40 == 20:
            score += cyc * reg
        
        reg += el
    return score


def task2(data):
    reg = 1
    lines = ""
    for cyc, el in cycle_iterate(data):
        if cyc % 40 == 1:
            lines += "\n"
        
        lines += ("█"
                  if abs( (cyc-1) % 40 - reg ) <= 1 else
                  "░")
        reg += el
    return lines


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
