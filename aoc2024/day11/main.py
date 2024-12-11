import math
from collections import defaultdict

from aoc_helper.utils import ExclusiveTimeIt, load_lines

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> defaultdict[int, int]:
    stones = defaultdict(int)
    for el in lines[0].split():
        stones[int(el)] += 1
    return stones


@timeit
def task(stones: defaultdict[int, int], steps: int) -> int:
    for _ in range(steps):
        new_stones = defaultdict(int)
        for num, count in stones.items():
            if num == 0:
                new_stones[1] += count
            elif (ndigits := (math.floor(math.log10(num)) + 1)) % 2 == 0:
                split = 10 ** (ndigits // 2)
                new_stones[num % split] += count
                new_stones[num // split] += count
            else:
                new_stones[2024 * num] += count
        stones = new_stones
    return sum(stones.values())


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task(inp, steps=25)
    total_p2 = task(inp, steps=75)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
