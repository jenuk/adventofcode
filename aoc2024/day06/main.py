from typing import Literal, overload

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]):
    n, m = len(lines), max(map(len, lines))
    starting_pos = None
    grid = [[False] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if lines[i][j] == "#":
                grid[i][j] = True
            elif lines[i][j] == "^":
                assert starting_pos is None
                starting_pos = (i, j)
    assert starting_pos is not None

    return grid, starting_pos


@overload
def task1(
    grid: list[list[bool]],
    starting_pos: tuple[int, int],
    return_marked: Literal[False] = False,
) -> int: ...


@overload
def task1(
    grid: list[list[bool]],
    starting_pos: tuple[int, int],
    return_marked: Literal[True] = True,
) -> tuple[int, list[list[bool]]]: ...


@timeit
def task1(
    grid: list[list[bool]], starting_pos: tuple[int, int], return_marked: bool = False
) -> int | tuple[int, list[list[bool]]]:
    n, m = len(grid), len(grid[0])

    def is_inside(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m

    dirs = [[set() for _ in range(m)] for _ in range(n)]
    x, y = starting_pos
    dx, dy = -1, 0
    while is_inside(x, y):
        if (dx, dy) in dirs[x][y]:
            if return_marked:
                marked = [[len(x) > 0 for x in line] for line in dirs]
                return -1, marked
            else:
                return -1
        dirs[x][y].add((dx, dy))
        x1, y1 = x + dx, y + dy
        while is_inside(x1, y1) and grid[x1][y1]:
            dx, dy = dy, -dx
            x1, y1 = x + dx, y + dy
        x, y = x1, y1

    if return_marked:
        marked = [[len(x) > 0 for x in line] for line in dirs]
        return sum(map(sum, marked)), marked
    else:
        return sum(len(x) > 0 for line in dirs for x in line)


@timeit
def task2(grid: list[list[bool]], starting_pos: tuple[int, int]) -> int:
    result = 0
    _, marked = task1(grid, starting_pos, return_marked=True)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if not marked[i][j] or (i, j) == starting_pos:
                continue
            grid[i][j] = True
            result += task1(grid, starting_pos) == -1
            grid[i][j] = False
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
