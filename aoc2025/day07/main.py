from enum import Enum

from aoc_helper.grid import Grid
from aoc_helper.utils import ExclusiveTimeIt, load_lines

timeit = ExclusiveTimeIt()


class States(Enum):
    empty = 0
    start = 1
    split = 2
    beam = 4

    @staticmethod
    def from_string(ch: str):
        if ch == "S":
            return States.start
        elif ch == "^":
            return States.split
        elif ch == "|":
            return States.beam
        else:
            return States.empty

    def __str__(self) -> str:
        if self is States.start:
            return "S"
        elif self is States.split:
            return "^"
        elif self is States.beam:
            return "|"
        else:
            return "."


def str_grid(grid: Grid[States]) -> str:
    res = ""
    for i in range(grid.n):
        for j in range(grid.m):
            res += str(grid[i, j])
        res += "\n"
    return res


@timeit
def prepare_input(lines: list[str]) -> Grid[States]:
    return Grid(
        len(lines), len(lines[0]), fn=lambda i, j: States.from_string(lines[i][j])
    )


@timeit
def task1(grid: Grid[States]) -> int:
    result = 0
    grid = grid.copy()
    for i in range(grid.n - 1):
        for j in range(grid.m):
            if grid[i, j] == States.beam or grid[i, j] == States.start:
                if grid[i + 1, j] == States.empty:
                    grid.safe_set(i + 1, j, States.beam)
                elif grid[i + 1, j] == States.split:
                    splits = grid.get(i + 1, j - 1, States.beam) == States.empty
                    splits |= grid.get(i + 1, j + 1, States.beam) == States.empty
                    grid.safe_set(i + 1, j - 1, States.beam)
                    grid.safe_set(i + 1, j + 1, States.beam)
                    result += splits
    return result


@timeit
def task2(grid: Grid[States]) -> int:
    grid_counts = Grid(
        grid.n, grid.m, fn=lambda i, j: 1 if grid[i, j] == States.start else 0
    )
    for i in range(grid.n - 1):
        for j in range(grid.m):
            beams = grid_counts[i, j]
            if beams > 0:
                if grid[i + 1, j] == States.empty:
                    grid_counts.safe_set(
                        i + 1,
                        j,
                        beams + grid_counts.get(i + 1, j, 0),
                    )
                elif grid[i + 1, j] == States.split:
                    grid_counts.safe_set(
                        i + 1,
                        j - 1,
                        beams + grid_counts.get(i + 1, j - 1, 0),
                    )
                    grid_counts.safe_set(
                        i + 1,
                        j + 1,
                        beams + grid_counts.get(i + 1, j + 1, 0),
                    )
    result = sum(grid_counts[grid.n - 1, j] for j in range(grid.m))
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
