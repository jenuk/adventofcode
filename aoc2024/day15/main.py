from enum import Enum

from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.grid import Grid

timeit = ExclusiveTimeIt()


class Cell(Enum):
    Empty = "."
    Wall = "#"
    Box = "O"
    BoxLeft = "["
    BoxRight = "]"


class Direction(Enum):
    Down = (1, 0)
    Up = (-1, 0)
    Left = (0, -1)
    Right = (0, 1)

    @classmethod
    def from_string(cls, ch: str):
        str_dict = {
            "v": cls.Down,
            "^": cls.Up,
            ">": cls.Right,
            "<": cls.Left,
        }
        return str_dict[ch]


@timeit
def prepare_input(lines: list[str]) -> tuple[Grid[Cell], list[Direction], int, int]:
    empty_idx = lines.index("")
    instructions = "".join(lines[empty_idx + 1 :])
    instructions = list(map(Direction.from_string, instructions))

    py = [idx for idx, line in enumerate(lines[:empty_idx]) if "@" in line][0]
    px = lines[py].index("@")
    lines[py] = lines[py].replace("@", ".")

    n = empty_idx
    m = len(lines[0])
    grid = Grid(n, m, fn=lambda i, j: Cell(lines[i][j]))
    return grid, instructions, py, px


def score(grid: Grid[Cell]) -> int:
    result = 0
    for i, j, cell in grid:
        if cell is Cell.Box or cell is Cell.BoxLeft:
            result += 100 * i + j
    return result


def print_grid(grid: Grid[Cell], py, px):
    result = ""
    for i in range(grid.n):
        for j in range(grid.m):
            if i == py and j == px:
                if grid[i, j] is not Cell.Empty:
                    print(i, j, grid[i, j], "should be '@'")

                result += "@"
            else:
                result += grid[i, j].value
        result += "\n"
    print(result)


@timeit
def task1(grid: Grid[Cell], instructions: list[Direction], py: int, px: int) -> int:
    grid = grid.copy()
    for inst in instructions:
        dy, dx = inst.value
        field = grid.get(py + dy, px + dx, Cell.Wall)
        if field is Cell.Empty:
            py, px = py + dy, px + dx
        elif field is Cell.Box:
            for k in range(2, max(grid.n, grid.m)):
                new_field = grid.get(py + k * dy, px + k * dx, Cell.Wall)
                if new_field is Cell.Wall:
                    break
                elif new_field is Cell.Empty:
                    grid[py + dy, px + dx] = Cell.Empty
                    grid[py + k * dy, px + k * dx] = Cell.Box
                    py, px = py + dy, px + dx
                    break
    return score(grid)


@timeit
def task2(grid: Grid[Cell], instructions: list[Direction], py: int, px: int) -> int:
    def expand(i: int, j: int):
        cell = grid[i, j // 2]
        if cell is Cell.Box:
            if j % 2 == 0:
                return Cell.BoxLeft
            else:
                return Cell.BoxRight
        else:
            return cell

    grid = Grid(grid.n, 2 * grid.m, fn=expand)
    px = 2 * px

    for inst in instructions:
        dy, dx = inst.value
        field = grid.get(py + dy, px + dx, Cell.Wall)
        if field is Cell.Empty:
            py, px = py + dy, px + dx
            continue
        elif field is Cell.Wall:
            continue

        if dy == 0:
            for k in range(2, max(grid.n, grid.m)):
                new_field = grid.get(py, px + k * dx, Cell.Wall)
                if new_field is Cell.Wall:
                    break
                elif new_field is Cell.BoxLeft or new_field is Cell.BoxRight:
                    continue

                for ux in range(px + k * dx, px, -dx):
                    grid[py, ux] = grid[py, ux - dx]
                py, px = py + dy, px + dx
                break
            continue

        intervals: dict[int, list[tuple[int, int | None]]] = {
            px: [(py + dy, None)],
            px + (1 if field is Cell.BoxLeft else -1): [(py + dy, None)],
        }
        wall = False
        for k in range(2, grid.n):
            for ux in list(intervals.keys()):
                if intervals[ux][-1][1] is not None:
                    continue

                new_field = grid.get(py + k * dy, ux, Cell.Wall)
                if new_field is Cell.Wall:
                    wall = True
                    break
                elif new_field is Cell.Empty:
                    intervals[ux][-1] = (intervals[ux][-1][0], py + k * dy)
                elif new_field is Cell.BoxLeft or new_field is Cell.BoxRight:
                    vx = ux + (1 if new_field is Cell.BoxLeft else -1)
                    if vx not in intervals:
                        intervals[vx] = [(py + k * dy, None)]
                    elif vx in intervals and intervals[vx][-1][1] is not None:
                        intervals[vx].append((py + k * dy, None))

            if wall:
                break

            if all(inter[-1][1] is not None for inter in intervals.values()):
                for ux, ints in intervals.items():
                    for uy_s, uy_e in ints:
                        assert uy_e is not None
                        for uy in range(uy_e, uy_s, -dy):
                            grid[uy, ux] = grid[uy - dy, ux]
                        grid[uy_s, ux] = Cell.Empty
                py, px = py + dy, px + dx
                break
    return score(grid)


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
