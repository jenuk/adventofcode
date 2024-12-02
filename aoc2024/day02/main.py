from functools import reduce
from typing import Generic, TypeVar, Union

from aoc_helper.utils import load_lines, timeit

T = TypeVar("T")


class SkipLine(Generic[T]):
    # SkipLine works as input too, but it's mostly added to avoid confusing
    # the type-checker. This is never used.
    def __init__(self, line: Union[list[T], "SkipLine[T]"], idx: int):
        self.line = line
        self.idx = idx

    def __len__(self):
        return len(self.line) - 1

    def __getitem__(self, idx: int) -> T:
        return self.line[idx + (idx >= self.idx)]


def is_safe(line: list[int] | SkipLine[int], dampen: bool) -> tuple[bool, bool]:
    if len(line) < 2:
        return (True, True)

    # check that we can get a sign below
    skipped_start = False
    if line[0] == line[1]:
        if dampen and line[0] != line[2]:
            line = SkipLine(line, 0)
            dampen = False
            skipped_start = True
        else:
            return (False, False)

    # expected generator direction.
    sign = line[1] - line[0]
    sign = sign / abs(sign)

    for k in range(len(line) - 1):
        if not (1 <= sign * (line[k + 1] - line[k]) <= 3):
            # either the general direction is wrong (case SkipLine(..., 0)) or we
            # need to skip either of the points in this set, otherwise it would be
            # impossible to dampen anything.  The eneral direction can only be
            # wrong if we are at the first comparision other than (line[0],
            # line[1]), i.e. k == 1
            return (
                False,
                dampen
                and (
                    is_safe(SkipLine(line, k), False)[0]
                    or is_safe(SkipLine(line, k + 1), False)[0]
                    or (k == 1 and is_safe(SkipLine(line, 0), False)[0])
                ),
            )

    # didn't find any broken places
    return (not skipped_start, True)


@timeit
def task1(lines: list[list[int]]) -> int:
    return sum(is_safe(line, False)[0] for line in lines)


@timeit
def task2(lines: list[list[int]]) -> int:
    return sum(is_safe(line, True)[1] for line in lines)


@timeit
def task_both(lines: list[list[int]]) -> tuple[int, int]:
    # same speed as task2 but solves both
    return reduce(
        lambda acc, val: (acc[0] + val[0], acc[1] + val[1]),
        (is_safe(line, True) for line in lines),
        (0, 0),
    )


@timeit
def main(fn: str):
    lines = load_lines(fn)
    lines = [list(map(int, line.split())) for line in lines]

    total_p1 = task1(lines)
    total_p2 = task2(lines)
    both = task_both(lines)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")
    print(f"Both: {both}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
