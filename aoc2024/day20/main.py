import itertools

from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.graph import bfs
from aoc_helper.grid import Grid

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[Grid[bool], tuple[int, int], tuple[int, int]]:
    start_px = [i for i, line in enumerate(lines) if "S" in line][0]
    start_py = lines[start_px].index("S")
    start = (start_px, start_py)
    lines[start_px] = lines[start_px].replace("S", ".")

    end_px = [i for i, line in enumerate(lines) if "E" in line][0]
    end_py = lines[end_px].index("E")
    end = (end_px, end_py)
    lines[end_px] = lines[end_px].replace("E", ".")

    grid = Grid(len(lines), len(lines[0]), fn=lambda i, j: lines[i][j] != "#")

    return grid, start, end


@timeit
def task1(
    grid: Grid[bool], start: tuple[int, int], end: tuple[int, int], threshold: int = 100
) -> int:
    result = 0
    graph = grid.to_graph(False, lambda i0, j0, i1, j1: grid[i0, j0] and grid[i1, j1])
    start_node = [node for node in graph if node.info == start][0]
    end_node = [node for node in graph if node.info == end][0]
    all_distances_start = {}
    for node, _, distance in bfs(start_node):
        all_distances_start[node.info] = distance
    all_distances_end = {}
    for node, _, distance in bfs(end_node):
        all_distances_end[node.info] = distance
    non_cheat_distance = all_distances_start[end]

    for (i0, j0), distance in all_distances_start.items():
        if distance + threshold + 2 > non_cheat_distance:
            continue

        for i1, j1, val in grid.get_neighbors(i0, j0):
            if val:
                continue

            for i2, j2, val in grid.get_neighbors(i1, j1):
                if not val:
                    continue

                total_distance = 2 + distance + all_distances_end[(i2, j2)]
                if total_distance + threshold <= non_cheat_distance:
                    result += 1
    return result


@timeit
def task2(
    grid: Grid[bool], start: tuple[int, int], end: tuple[int, int], threshold: int = 100
) -> int:
    result = 0
    graph = grid.to_graph(False, lambda i0, j0, i1, j1: grid[i0, j0] and grid[i1, j1])
    start_node = [node for node in graph if node.info == start][0]
    end_node = [node for node in graph if node.info == end][0]
    all_distances_start = {}
    for node, _, distance in bfs(start_node):
        all_distances_start[node.info] = distance
    all_distances_end = {}
    for node, _, distance in bfs(end_node):
        all_distances_end[node.info] = distance
    non_cheat_distance = all_distances_start[end]

    for (i0, j0), distance in all_distances_start.items():
        max_steps = max(min(non_cheat_distance + threshold - distance, 20), -1)

        for di in range(max_steps+1):
            for dj in range(max_steps+1 - di):
                for dir_i, dir_j in itertools.product(
                    [-1, 1] if di != 0 else [1],
                    [-1, 1] if dj != 0 else [1],
                ):
                    i1 = i0 + dir_i * di
                    j1 = j0 + dir_j * dj
                    new_distance = all_distances_end.get((i1, j1), None)
                    if new_distance is None:
                        continue

                    total_distance = distance + new_distance + di + dj
                    if total_distance + threshold <= non_cheat_distance:
                        result += 1
    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(*inp, threshold=100)
    total_p2 = task2(*inp, threshold=100)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
