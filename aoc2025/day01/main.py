from collections import defaultdict
import itertools

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> list[int]:
    return [((1 if l[0] == "R" else -1) * int(l[1:])) for l in lines]


@timeit
def task1(insts: list[int]) -> int:
    result = 0
    position = 50
    for count in insts:
        position = (position + count) % 100
        result += position == 0
    return result


@timeit
def task2(insts: list[int]) -> int:
    result = 0
    position = 50
    for count in insts:
        # special case that overcounts the starting 0 as crossed a second time
        result -= count < 0 and position == 0

        position = position + count
        result += abs((position - (count < 0)) // 100)
        position = position % 100
    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(inp)
    total_p2 = task2(inp)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
