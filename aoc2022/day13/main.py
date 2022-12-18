from __future__ import annotations

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

class Packet:
    def __init__(self, vals):
        if isinstance(vals, int):
            self.vals = vals
        else:
            self.vals = [Packet(v) for v in vals]

    def check_order(self, other: Packet) -> tuple[bool, bool]:
        if isinstance(self.vals, int) and isinstance(other.vals, int):
            return self.vals < other.vals, self.vals == other.vals
        elif isinstance(self.vals, list) and isinstance(other.vals, list):
            for el1, el2 in zip(self.vals, other.vals):
                val, cont = el1.check_order(el2)
                if not cont:
                    return val, False
            return (len(self.vals) < len(other.vals),
                    len(self.vals) == len(other.vals))
        elif isinstance(self.vals, int):
            return Packet([self.vals]).check_order(other)
        else:
            return self.check_order(Packet([other.vals]))

    def __lt__(self, other: Packet):
        return self.check_order(other)[0]

    def __eq__(self, other: Packet) -> bool:
        return self.vals == other.vals

    def __le__(self, other: Packet):
        return (self < other) or (self == other)


def process_data(content):
    pairs = content.split("\n\n")
    data = []
    for p in pairs:
        a, b = p.split("\n")
        data.append([Packet(eval(a)), Packet(eval(b))])
    return data


def check_data(data):
    pass


def task1(data):
    result = 0
    for k, (p1, p2) in enumerate(data):
        result += (k+1)*(p1 <= p2)
    return result


def task2(data):
    flattened = [p for pair in data for p in pair]
    div1 = Packet([[2]])
    div2 = Packet([[6]])
    flattened.append(div1)
    flattened.append(div2)
    flattened.sort()
    return (flattened.index(div1)+1)*(flattened.index(div2)+1)


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
