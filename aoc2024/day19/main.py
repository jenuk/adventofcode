import heapq
from collections import defaultdict
from aoc_helper.graph import BaseNode, dfs
from aoc_helper.utils import load_lines, ExclusiveTimeIt

from typing import Hashable, Iterator

timeit = ExclusiveTimeIt()


class CombinationNode(BaseNode):
    has_unique = True

    def __init__(self, combination: str, all_towels: list[str]):
        self.combination = combination
        self.all_towels = all_towels

    def unique(self) -> Hashable:
        return self.combination

    def get_neighbors(self, reverse: bool = False) -> "Iterator[CombinationNode]":
        if reverse:
            for towel in self.all_towels:
                yield CombinationNode(towel + self.combination, self.all_towels)
        else:
            for towel in self.all_towels:
                if self.combination.startswith(towel):
                    yield CombinationNode(
                        self.combination[len(towel) :], self.all_towels
                    )

    def __str__(self) -> str:
        return f"Node({self.combination})"


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[list[str], list[str]]:
    towels = lines[0].split(", ")
    lines = lines[2:]
    return towels, lines


@timeit
def task1(towels: list[str], lines: list[str]) -> int:
    towels = sorted(towels, key=lambda s: len(s))
    result = 0
    for combination in lines:
        node = CombinationNode(combination, towels)
        for other, _ in dfs(node):
            if other.combination == "":
                result += 1
                break
    return result


@timeit
def task2(towels: list[str], lines: list[str]) -> int:
    all_starts = {comb[:k] for comb in lines for k in range(len(comb)+1)}
    max_length = max(map(len, lines))
    result = 0
    last = {towel: 1 for towel in towels}
    for _ in range(max_length):
        current = defaultdict(int)
        for prev, count in last.items():
            for towel in towels:
                new = prev + towel
                if new in all_starts:
                    current[new] += count

        if len(current) == 0:
            break

        result += sum(current[combination] for combination in lines)
        last = current

    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(*inp)
    total_p2 = task2(*inp)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
