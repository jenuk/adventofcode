from typing import Any, Iterator

from aoc_helper.graph_traversal import dijkstra
from aoc_helper.graph import BaseNode
from aoc_helper.utils import load_lines, timeit


class CityBlock(BaseNode):
    # a fancy tuple plus one pointer
    directions = [
        [-1, 0],
        [0, -1],
        [1, 0],
        [0, 1],
    ]

    def __init__(
        self,
        square: list[list[int]],
        px: int,
        py: int,
        vec: int,
        k: int,
        max_k: int,
        min_k: int,
    ):
        self.square = square
        self.px = px
        self.py = py
        self.vec = vec
        self.k = k
        self.max_k = max_k
        self.min_k = min_k

    @property
    def tup(self) -> tuple[int, ...]:
        return (self.px, self.py, self.k, self.vec)

    def __hash__(self):
        return hash(self.tup)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CityBlock):
            return False

        return self.tup == other.tup

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["CityBlock", int]]:
        assert not reverse, "Not implemented"
        for vec, (dx, dy) in enumerate(self.directions):
            # check if that step is available:
            # - x in bounds
            # - y in bounds
            # - don't go to long in a straight line
            # - don't turn around
            # - go at least min_k steps in one direction
            if (
                0 <= self.px + dx < len(self.square)
                and 0 <= self.py + dy < len(self.square[0])
                and (vec != self.vec or (self.k < self.max_k))
                and (vec != ((self.vec + 2) % 4))
                and (self.k >= self.min_k or vec == self.vec or self.vec == -1)
            ):
                yield (
                    (
                        CityBlock(
                            self.square,
                            self.px + dx,
                            self.py + dy,
                            vec,
                            self.k + 1 if self.vec == vec else 1,
                            self.max_k,
                            self.min_k,
                        ),
                        self.square[self.px + dx][self.py + dy],
                    )
                )


@timeit
def main(fn: str):
    lines = load_lines(fn)
    square = [list(map(int, line)) for line in lines]
    n, m = len(square), len(square[0])

    total_p1 = 0
    total_p2 = 0

    start = CityBlock(square, 0, 0, -1, 0, 3, 0)
    for node, _, distance in dijkstra(start, start_weight=0):
        if node.px == n - 1 and node.py == m - 1:
            total_p1 = distance
            break
    else:
        print("No solution found (p1)")

    start = CityBlock(square, 0, 0, -1, 0, 10, 4)
    for node, _, distance in dijkstra(start, start_weight=0):
        if node.px == n - 1 and node.py == m - 1:
            total_p2 = distance
            break
    else:
        print("No solution found (p2)")

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
