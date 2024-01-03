from itertools import cycle
from time import perf_counter_ns
from typing import Iterator, Optional
from typing_extensions import Self

import sys

sys.setrecursionlimit(12_000)


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


class LinkedList:
    def __init__(
        self,
        source: list,
        total_length: int,
        start: Optional[Self] = None,
        left: Optional[Self] = None,
        multiply: int = 1,
    ):
        if left is None:
            assert start is None
            # don't know last element yet, placeholder
            left = self
            start = self
        assert left is not None and start is not None
        self.val = source[0] * multiply
        self.left = left
        self.total_length = total_length
        if len(source) > 1:
            self.right = LinkedList(
                source[1:], total_length, start, self, multiply=multiply
            )
        else:
            self.right = start
            start.left = self

    def __iter__(self) -> Iterator[Self]:
        yield self
        current = self.right
        while current != self:
            yield current
            current = current.right

    def get_nn(self) -> Self:
        for node in self:
            if node.val == 0:
                return node
        raise ValueError("Null node went missing")

    def move(self):
        # choose left- or right-way around based on length
        val_p = self.val % (self.total_length - 1)
        val_n = (self.total_length - 1) - val_p
        if val_p < val_n:
            val = val_p
            left = self
            for _ in range(val):
                left = left.right
            right = left.right
        else:
            val = val_n
            val = (-self.val) % (self.total_length - 1)
            right = self
            for _ in range(val):
                right = right.left
            left = right.left
        if self == left or self == right:
            return

        # remove self
        prev_left = self.left
        prev_right = self.right
        prev_left.right = prev_right
        prev_right.left = prev_left

        # insert self at new place
        right.left = self
        left.right = self
        self.right = right
        self.left = left

    def __str__(self):
        return " -> ".join(str(n.val) for n in self)


def process_data(content):
    lines = content.split("\n")
    vals = list(map(int, lines))
    return vals


def check_data(data):
    assert sum(1 for n in data if n == 0) == 1


def get_num(ll: LinkedList, num_nodes: int) -> int:
    null_node = ll.get_nn()
    result = 0
    final_pos = {1000 % num_nodes, 2000 % num_nodes, 3000 % num_nodes}
    for k, current in enumerate(null_node):
        if k in final_pos:
            result += current.val
    return result


def task1(data):
    ll = LinkedList(data, len(data))
    nodes = [n for n in ll]
    for node in nodes:
        node.move()
    return get_num(ll, len(nodes))


def task2(data):
    ll = LinkedList(data, len(data), multiply=811589153)
    nodes = [n for n in ll]
    for _ in range(10):
        for node in nodes:
            node.move()
    return get_num(ll, len(nodes))


def main():
    # fn = "example"
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
