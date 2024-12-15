from aoc_helper.grid import Grid
from aoc_helper.graph import bfs
from aoc_helper.utils import load_lines, timeit


@timeit
def prepare_input(lines: list[str]) -> Grid[str]:
    n, m = len(lines), len(lines[0])
    return Grid(n, m, fn=lambda i, j: lines[i][j])


@timeit
def task1(grid: Grid[str]) -> int:
    graph = grid.to_graph(
        False,
        is_connected=lambda i0, j0, i1, j1: grid[i0, j0] == grid[i1, j1],
    )

    result = 0
    found = Grid(grid.n, grid.m, fn=lambda i, j: False)
    for node in graph:
        if found[node.info]:
            continue

        current_perimeter = 0
        current_area = 0
        for other, _, _ in bfs(node):
            found[other.info] = True
            current_perimeter += 4 - len(other.outgoing)
            current_area += 1
        result += current_area * current_perimeter
    return result


@timeit
def task2(grid: Grid[str]) -> int:
    graph = grid.to_graph(
        False,
        is_connected=lambda i0, j0, i1, j1: grid[i0, j0] == grid[i1, j1],
    )

    result = 0
    found = Grid(grid.n, grid.m, fn=lambda i, j: False)
    for node in graph:
        if found[node.info]:
            continue
        edges = Grid(grid.n, grid.m, fn=lambda i, j: tuple())

        current_area = 0
        for other, _, _ in bfs(node):
            found[other.info] = True
            for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                edges[other.info] += (
                    grid[other.info]
                    != grid.get(other.info[0] + dx, other.info[1] + dy, None),
                )
            current_area += 1

        current_sides = 0
        for k in range(2):
            for i in range(grid.n):
                last = False
                for j in range(grid.m):
                    current = len(edges[i, j]) == 4 and edges[i, j][k]
                    if last != current:
                        last = current
                        current_sides += last

            for j in range(grid.m):
                last = False
                for i in range(grid.n):
                    current = len(edges[i, j]) == 4 and edges[i, j][2 + k]
                    if last != current:
                        last = current
                        current_sides += last

        result += current_area * current_sides
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
