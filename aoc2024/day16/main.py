import operator
from enum import Enum
from typing import Iterator
from aoc_helper.graph.distance import dijkstra2
from aoc_helper.graph.utils import to_explicit
from typing_extensions import Self

from aoc_helper.grid import Grid
from aoc_helper.graph import BaseNode, dijkstra
from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.vector import scalar_vec, vec_op

timeit = ExclusiveTimeIt()


class Cell(Enum):
    Empty = "."
    Wall = "#"


class ReinderState(BaseNode[int]):
    has_unique = True

    def __init__(
        self,
        grid: Grid[Cell],
        loc: tuple[int, int],
        direction: tuple[int, int],
    ):
        self.grid = grid
        self.loc = loc
        self.direction = direction

    def unique(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (self.loc, self.direction)

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple[Self, int]]:
        assert not reverse, "Not Implemented"
        neg_direction = scalar_vec(-1, self.direction)
        for i, j, val in self.grid.get_neighbors(*self.loc):
            if val is Cell.Wall:
                continue
            new_direction = vec_op((i, j), self.loc, operator.sub)
            if new_direction == neg_direction:
                continue
            score = 1 + 1000 * (new_direction != self.direction)
            yield ReinderState(self.grid, (i, j), new_direction), score


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[Grid[Cell], tuple[int, int], tuple[int, int]]:
    start_px = [i for i, line in enumerate(lines) if "S" in line][0]
    start_py = lines[start_px].index("S")
    start = (start_px, start_py)
    lines[start_px] = lines[start_px].replace("S", ".")

    end_px = [i for i, line in enumerate(lines) if "E" in line][0]
    end_py = lines[end_px].index("E")
    end = (end_px, end_py)
    lines[end_px] = lines[end_px].replace("E", ".")

    grid = Grid(len(lines), len(lines[0]), fn=lambda i, j: Cell(lines[i][j]))

    return grid, start, end


@timeit
def task1(grid: Grid[Cell], start: tuple[int, int], end: tuple[int, int]) -> int:
    state = ReinderState(grid, start, (0, 1))
    for node, _, score in dijkstra(state):
        if node.loc == end:
            return score
    return -1


@timeit
def task2(grid: Grid[Cell], start: tuple[int, int], end: tuple[int, int]) -> int:
    state = ReinderState(grid, start, (0, 1))
    explicit_graph, _ = to_explicit(state)

    end_nodes = [(k, e) for k, e in enumerate(explicit_graph) if e.info.loc == end]
    assert len(end_nodes) == 1, "Was given in my case"
    end_idx, end_node = end_nodes[0]

    _, distances_start = dijkstra2(explicit_graph[0], explicit_graph)
    _, distances_end = dijkstra2(end_node, explicit_graph, reverse=True)
    min_distances = distances_start[end_idx]

    is_best_path = Grid(grid.n, grid.m, fn=lambda i, j: False)
    for k, node in enumerate(explicit_graph):
        if distances_start[k] + distances_end[k] == min_distances:
            is_best_path[node.info.loc] = True

    return sum(val for _, _, val in is_best_path)


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
