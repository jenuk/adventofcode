from aoc_helper.graph.traversal import BaseNode
from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.grid import Grid
from aoc_helper.graph import dijkstra

from typing import Iterator

timeit = ExclusiveTimeIt()


class DynamicNode(BaseNode[int]):
    has_unique = True

    def __init__(
        self, grid: Grid[bool], grid_nodes: "Grid[DynamicNode]", idx: tuple[int, int]
    ):
        self.grid_nodes = grid_nodes
        self.grid = grid
        self.idx = idx

    def unique(self):
        return self.idx

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["DynamicNode", int]]:
        if reverse and not self.grid[self.idx]:
            return

        for i, j, val in self.grid.get_neighbors(*self.idx):
            if not val:
                continue
            yield (self.grid_nodes[i, j], 1)


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[list[tuple[int, int]], Grid[bool], Grid[DynamicNode]]:
    all_bytes = [(int((t := line.split(","))[0]), int(t[1])) for line in lines]
    grid = Grid(71, 71, fn=lambda i, j: True)
    node_grid: Grid[DynamicNode] = Grid(71, 71, fn=lambda i, j: None)
    for i in range(grid.n):
        for j in range(grid.m):
            node_grid[i, j] = DynamicNode(grid, node_grid, (i, j))
    return (all_bytes, grid, node_grid)


@timeit
def task1(all_bytes: list[tuple[int, int]], grid: Grid[bool], grid_nodes: Grid[DynamicNode]) -> int:
    for loc in all_bytes[:1024]:
        grid[loc] = False

    start = grid_nodes[0, 0]
    end = grid_nodes[70, 70]
    for node, _, dist in dijkstra(start):
        if node is end:
            return dist
    return -1


@timeit
def task2(all_bytes: list[tuple[int, int]], grid: Grid[bool], node_grid: Grid[DynamicNode]) -> str:
    start = node_grid[0, 0]
    end = node_grid[70, 70]

    max_byte = 1023
    path: set[tuple[int, int]] | None = None
    while max_byte < len(all_bytes):
        max_byte += 1
        grid[all_bytes[max_byte]] = False
        if path is None or all_bytes[max_byte] in path:
            all_parents = dict()

            for node, parent, _ in dijkstra(start):
                all_parents[node] = parent
                if node is end:
                    break
            else:
                return ",".join(map(str, all_bytes[max_byte]))

            path = set()
            current = end
            while current is not start:
                path.add(current.idx)
                current = all_parents[current]

    return "None"


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
