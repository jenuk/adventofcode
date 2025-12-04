from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.grid import Grid

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> Grid[bool]:
    n = len(lines)
    m = len(lines[0])
    values = [[x == "@" for x in line] for line in lines]
    return Grid(n, m, values=values)


@timeit
def task1(grid: Grid[bool]) -> int:
    result = 0
    for i, j, full in grid:
        if not full:
            continue

        full_neighbors = sum(x for _, _, x in grid.get_diagonal_neighbors(i, j))
        result += full_neighbors < 4
    return result


@timeit
def task2(grid: Grid[bool]) -> int:
    result = 0
    grid = grid.copy()
    stack = [(i, j) for i, j, full in grid if full]
    while stack:
        i, j = stack.pop()
        if not grid[i, j]:
            continue

        full_neighbors = sum(x for _, _, x in grid.get_diagonal_neighbors(i, j))
        if full_neighbors < 4:
            result += 1
            grid[i, j] = False
            stack.extend((i, j) for i, j, x in grid.get_diagonal_neighbors(i, j) if x)
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
