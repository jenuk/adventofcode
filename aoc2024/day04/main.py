import functools
import itertools

from aoc_helper.utils import load_lines, timeit


def check_slice(
    lines: list[str],
    i: int,
    j: int,
    deltas: list[tuple[int, int]],
    word: str,
) -> bool:
    for ch, (di, dj) in zip(word, deltas):
        i1, j1 = i + di, j + dj
        if not (0 <= i1 < len(lines) and 0 <= j1 < len(lines[i1])):
            return False
        elif lines[i1][j1] != ch:
            return False
    return True


# this is probably not a good pattern for actual code, but looked like a
# fun idea: basically prepare some context variable in a local scope without
# having to recompute them every time
# also not sure how to type-annotate this
@lambda f: functools.wraps(f)(f())
def check_p1():
    word = "MAS"
    directions = [
        [(dx * i, dy * i) for i in range(1, len(word) + 1)]
        for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1])
        if dx != 0 or dy != 0
    ]
    # gives all possible directions form the center to the left, right, up, down
    # left-up, left-down, right-up, right-down. Since the rate of change in each
    # variable is always 1, 0, or -1

    def inner(lines: list[str], i: int, j: int) -> int:
        # always check from the starting point X in all directions instead of
        # looking for the inverse word samx only to the right
        if lines[i][j] != "X":
            return 0

        total = 0
        for deltas in directions:
            total += check_slice(lines, i, j, deltas, word)
        return total

    return inner


@timeit
def task1(lines: list[str]) -> int:
    result = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            result += check_p1(lines, i, j)
    return result


@lambda f: functools.wraps(f)(f())
def check_p2():
    word = "MS"
    # we are looking at
    # (-1, -1) (------) (-1,  1)
    # (------) (------) (------)
    # ( 1, -1) (------) ( 1,  1)
    # giving us (-1, -1) -- (1, 1)
    # and (1, -1) -- (-1, 1)
    # center is tested separately
    diagonals = [
        [(-1, -1), (1, 1)],
        [(1, -1), (-1, 1)],
    ]
    all_deltas_a = [diagonals[0], diagonals[0][::-1]]
    all_deltas_b = [diagonals[1], diagonals[1][::-1]]

    def inner(lines: list[str], i: int, j: int) -> int:
        # a x-mas is uniquely described by its middle points, so we search for
        # x-mas from that starting point, to avoid overcounting
        if lines[i][j] != "A":
            return 0

        # this makes use of short-circuts to test 2-4 conditions depending on
        # the needs. Could do this with loops, but since it's only two
        # possibility per diagonal, this is sufficiently clear.
        return (
            check_slice(lines, i, j, all_deltas_a[0], word)
            or check_slice(lines, i, j, all_deltas_a[1], word)
        ) and (
            check_slice(lines, i, j, all_deltas_b[0], word)
            or check_slice(lines, i, j, all_deltas_b[1], word)
        )

    return inner


@timeit
def task2(lines: list[str]) -> int:
    result = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            result += check_p2(lines, i, j)
    return result


@timeit
def main(fn: str):
    lines = load_lines(fn)

    total_p1 = task1(lines)
    total_p2 = task2(lines)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
