from __future__ import annotations

import re
from math import prod, gcd as gcd_tuple
from time import perf_counter_ns
from typing import Callable, Dict, List, Optional, Tuple

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

def parse_operation(operation: str) -> Callable[[int], int]:
    arg1, op, arg2 = operation.split(" ")
    assert arg1 == "old"
    if arg2 == "old":
        def inner_plus(x):
            return x + x
        
        def inner_times(x):
            return x * x
    else:
        n = int(arg2)
        def inner_plus(x):
            return x + n
        
        def inner_times(x):
            return x * n

    if op == "+":
        return inner_plus
    elif op == "*":
        return inner_times
    else:
        raise ValueError(f"Unknown operation '{op}'")

class Monkey:
    monkeys: List[Monkey] = list()

    def __init__(self, items, operation, test, ttarget, ftarget):
        self.items = items
        self.operation = operation
        self.test = test
        self.ttarget = ttarget
        self.ftarget = ftarget
        self.num_passes = 0

    def throw(self, chilled: bool=True, div: Optional[int]=None):
        for item in self.items:
            item = self.operation(item)
            if chilled:
                item = item//3
            if div is not None:
                item = item % div
            if item % self.test == 0:
                self.monkeys[self.ttarget].items.append(item)
            else:
                self.monkeys[self.ftarget].items.append(item)

        self.num_passes += len(self.items)
        self.items = []
    
    @staticmethod
    def from_string(inp: str) -> Tuple[int, Monkey]:
        pattern = (
            r"Monkey (?P<id>\d):\n"
            r"  Starting items: (?P<items>(?:\d+,? ?)*)\n"
            r"  Operation: new = (?P<op>.*)\n"
            r"  Test: divisible by (?P<test>\d+)\n"
            r"    If true: throw to monkey (?P<ttarget>\d)\n"
            r"    If false: throw to monkey (?P<ftarget>\d)"
        )
        pattern = re.compile(pattern, re.MULTILINE)
        match = re.match(pattern, inp)
        assert match is not None, f"invalid monkey:\n{inp}"
        m_id = int(match.group("id"))
        starting_items = list(map(int, match.group("items").split(",")))
        operation = parse_operation(match.group("op"))
        test = int(match.group("test"))
        ttarget = int(match.group("ttarget"))
        ftarget = int(match.group("ftarget"))
        monkey = Monkey(starting_items, operation, test, ttarget, ftarget)
        Monkey.monkeys[m_id] = monkey
        return m_id, monkey


def process_data(content: str) -> List[Monkey]:
    monkeys = content.split("\n\n")
    Monkey.monkeys = [None]*len(monkeys)
    for mstr in monkeys:
        _ = Monkey.from_string(mstr)
    return Monkey.monkeys


def check_data(data):
    pass


def top2(data: List[Monkey]) -> int:
    m = (data[0].num_passes, data[1].num_passes)
    if m[1] < m[0]:
        m = (m[1], m[0])
    for monkey in data[2:]:
        if monkey.num_passes > m[0]:
            if monkey.num_passes > m[1]:
                m = (m[1], monkey.num_passes)
            else:
                m = (monkey.num_passes, m[1])
    return m[0]*m[1]


def task1(data: List[Monkey]) -> int:
    for _ in range(20):
        for monkey in data:
            monkey.throw()
    return top2(data)


def gcd(*ints: int) -> int:
    # still on python 3.8, math.gcd only accepts two arguments
    if len(ints) == 0:
        return 1
    res = ints[0]
    for k in ints[1:]:
        res = gcd_tuple(res, k)
    return res


def task2(data: List[Monkey]) -> int:
    div = prod(m.test for m in data)
    # doesn't change anything for my data, but is nice in general
    div = div // gcd(*tuple(m.test for m in data))
    for _ in range(10_000):
        for monkey in data:
            monkey.throw(False, div)
    return top2(data)


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
    check_data(data)
    t1 = perf_counter_ns()
    result1 = task1(data)
    t2 = perf_counter_ns()
    # reset data
    data = read_data(fn)
    result2 = task2(data)
    t3 = perf_counter_ns()

    print(f"Data preprocessing in {format_ns(t1 - t0)}")
    print(f"Task 1: {result1} in {format_ns(t2 - t1)}")
    print(f"Task 2: {result2} in {format_ns(t3 - t2)}")


if __name__ == "__main__":
    main()
