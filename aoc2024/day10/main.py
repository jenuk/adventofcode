from collections import deque

from aoc_helper.graph import ExplicitNode, bfs
from aoc_helper.utils import ExclusiveTimeIt, load_lines
from aoc_helper.grid import Grid

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> tuple[Grid[int], list[ExplicitNode]]:
    grid = Grid(
        len(lines),
        len(lines[0]),
        fn=lambda i, j: int(lines[i][j]),
    )
    graph = grid.to_graph(
        diagonal=False,
        is_connected=lambda i0, j0, i1, j1: grid[i1, j1] - grid[i0, j0] == 1,
    )
    return grid, graph


@timeit
def task1(grid: Grid[int], graph: list[ExplicitNode]) -> int:
    result = 0
    for node in graph:
        if grid[node.info] != 0:
            continue
        score = 0
        for other, _, _ in bfs(node):
            if grid[other.info] == 9:
                score += 1
        result += score
    return result


@timeit
def task2(grid: Grid[int], graph: list[ExplicitNode]) -> int:
    nodes_by_level = [[] for _ in range(10)]
    for node in graph:
        nodes_by_level[grid[node.info]].append(node)
    grid_ratings = Grid(grid.n, grid.m, fn=lambda i, j: int(grid[i, j] == 9))

    for nodes in nodes_by_level[-2::-1]:
        for node in nodes:
            grid_ratings[node.info] = sum(
                grid_ratings[neighbor.info] for neighbor in node.get_neighbors()
            )

    return sum(grid_ratings[node.info] for node in nodes_by_level[0])


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
