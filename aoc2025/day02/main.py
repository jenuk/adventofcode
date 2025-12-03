import math

from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.math import gauss_sum

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> list[tuple[int, int]]:
    assert len(lines) == 1, "Invalid input"
    return [tuple(map(int, t.split("-"))) for t in lines[0].split(",")]


def bisect_smallest(a, b, check) -> int:
    assert check(b)
    while a < b:
        m = (a + b) // 2
        if check(m):
            b = m
        else:
            a = m + 1
    return b


def bisect_biggest(a, b, check) -> int:
    assert check(a)
    while a < b:
        m = math.ceil((a + b) / 2)
        if check(m):
            a = m
        else:
            b = m - 1
    return a


@timeit
def task1(intervals: list[tuple[int, int]]) -> int:
    result = 0
    for a, b in intervals:
        min_digits = max(math.ceil(math.ceil(math.log10(a)) / 2), 1)
        max_digits = math.floor(math.ceil(math.log10(b)) / 2)
        for num_digits in range(min_digits, max_digits + 1):
            check = lambda x: x + x * 10**num_digits >= a
            min_solution = bisect_smallest(
                10 ** (num_digits - 1),
                10**num_digits - 1,
                check,
            )
            check = lambda x: x + x * 10**num_digits <= b
            max_solution = bisect_biggest(
                10 ** (num_digits - 1), 10**num_digits - 1, check
            )
            result += int(10**num_digits + 1) * (
                gauss_sum(max_solution) - gauss_sum(min_solution - 1)
            )

    return result


@timeit
def task2(intervals: list[tuple[int, int]]) -> int:
    result = 0
    for a, b in intervals:
        max_repeats = math.ceil(math.log10(b))
        all_solutions = set()
        for num_repeats in range(2, max_repeats + 1):
            min_digits = max(math.ceil(math.ceil(math.log10(a)) / num_repeats), 1)
            max_digits = math.ceil(math.log10(b)) // num_repeats
            for num_digits in range(min_digits, max_digits + 1):
                pattern_number = 0
                for _ in range(num_repeats):
                    pattern_number = pattern_number * int(10 ** (num_digits)) + 1

                try:
                    min_solution = bisect_smallest(
                        10 ** (num_digits - 1),
                        10**num_digits - 1,
                        lambda x: x * pattern_number >= a,
                    )
                    max_solution = bisect_biggest(
                        10 ** (num_digits - 1),
                        10**num_digits - 1,
                        lambda x: x * pattern_number <= b,
                    )
                    if min_solution > max_solution:
                        continue

                    # because of the different repetitions, we might get
                    # duplicate numbers, e.g. 2 repeated 3 times with 2 digits
                    # each or 2 repeated 6 times with 1 digit each both produce
                    # 222222. Since there are not a lot numbers per range, we
                    # can just track all of them explicitly.
                    all_solutions.update(
                        pattern_number * x
                        for x in range(min_solution, max_solution + 1)
                    )
                except AssertionError:
                    # the minimum with the current pattern is too big
                    continue
        result += sum(all_solutions)

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
