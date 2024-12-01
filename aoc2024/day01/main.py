from collections import defaultdict

from aoc_helper.utils import load_lines, timeit


@timeit
def task1(lines: list[tuple[int, int]]) -> int:
    left = [a for a, _ in lines]
    right = [b for _, b in lines]
    left.sort()
    right.sort()
    return sum(abs(a - b) for a, b in zip(left, right))


@timeit
def task2(lines: list[tuple[int, int]]) -> int:
    left = [a for a, _ in lines]
    right = [b for _, b in lines]

    counts = defaultdict(int)
    for b in right:
        counts[b] += 1

    return sum(a * counts[a] for a in left)


@timeit
def main(fn: str):
    lines = load_lines(fn)
    lines = [(int((t := line.split())[0]), int(t[1])) for line in lines]

    total_p1 = task1(lines)
    total_p2 = task2(lines)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
