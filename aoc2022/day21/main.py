from typing_extensions import Self
from time import perf_counter_ns
from fractions import Fraction


# Ignore below


def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 0
    prev = 0
    while time > lengths[idx + 1]:
        idx += 1
        time, prev = time // lengths[idx], time % lengths[idx]

    out = f"{time}{units[idx]}"
    if 0 < prev and time < 100:
        out += f" {prev}{units[idx-1]}"
    return out


def read_data(filename="input.txt"):
    with open(filename) as file:
        content = file.read().strip()

    return process_data(content)


# Ignore above


def process_data(content: str):
    monkeys = {}
    for line in content.split("\n"):
        name, instruction = line.split(": ")
        monkeys[name] = Monkey(name, instruction, monkeys)
        if name == "humn":
            monkeys["humn_val"] = int(instruction)
    return monkeys


def check_data(data):
    pass


op_dict = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "=": lambda a, b: a == b,
}


class LinearFn:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def __add__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(self.m, self.b + other)

    def __radd__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(self.m, self.b + other)

    def __sub__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(self.m, self.b - other)

    def __rsub__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(-self.m, other - self.b)

    def __mul__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(self.m * other, self.b * other)

    def __rmul__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(self.m * other, self.b * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, Fraction)):
            return NotImplemented
        return LinearFn(self.m / other, self.b / other)

    def __str__(self):
        return f"{self.m} * x + {self.b}"

    def __call__(self, x):
        return self.m * x + self.b


class Monkey:
    def __init__(self, name: str, val: str, monkeys: dict[str, Self]):
        self.monkeys = monkeys
        self.name = name
        if val.isnumeric():
            self.is_instruction = False
            if name == "humn":
                self.orig_val = int(val)
                self.val = LinearFn(Fraction(1), Fraction(0))
            else:
                self.val = Fraction(int(val))
            self.left, self.op, self.right = "", "", ""
        else:
            self.is_instruction = True
            self.val = None
            self.left, self.op, self.right = val.split(" ")

    def solve(self):
        if self.val is not None:
            # end of tree
            return
        left = self.monkeys[self.left]
        right = self.monkeys[self.right]
        left.solve()
        right.solve()
        self.val = op_dict[self.op](left.val, right.val)


def task1(monkeys):
    root = monkeys["root"]
    humn = monkeys["humn_val"]
    root.solve()
    return int(root.val(humn))


def task2(monkeys):
    root = monkeys["root"]
    left = monkeys[root.left]
    right = monkeys[root.right]

    # this is already done in task1, so it won't be computed again
    left.solve()
    right.solve()

    # solve linear equation
    total = left.val - right.val
    humn = -total.b / total.m
    return humn


def main():
    # fn = "input_bsp.txt"
    fn = "input"
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
