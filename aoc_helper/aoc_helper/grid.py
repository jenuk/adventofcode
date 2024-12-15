import itertools
from typing import Callable, Iterator, TypeVar, Generic

from .graph import ExplicitNode

S = TypeVar("S")
T = TypeVar("T")


class Grid(Generic[T]):
    def __init__(
        self,
        n: int,
        m: int,
        values: list[list[T]] | None = None,
        fn: Callable[[int, int], T] | None = None,
    ):
        assert (fn is None) != (values is None)
        self.n = n
        self.m = m
        if values is not None:
            self.data = values
        else:
            assert fn is not None
            self.data = []
            for i in range(n):
                self.data.append([])
                for j in range(m):
                    self.data[-1].append(fn(i, j))

    def copy(self) -> "Grid[T]":
        return Grid(self.n, self.m, fn=lambda i, j: self[i, j])

    def __getitem__(self, idx: tuple[int, int]) -> T:
        i, j = idx
        if not self.is_inside(*idx):
            raise IndexError(
                f"Index {idx} out of bounds for Grid with dims {self.n} x {self.m}"
            )
        return self.data[i][j]

    def __setitem__(self, idx: tuple[int, int], val: T):
        if not self.is_inside(*idx):
            raise IndexError(
                f"Index {idx} out of bounds for Grid with dims {self.n} x {self.m}"
            )
        self.data[idx[0]][idx[1]] = val

    def get_neighbors(self, i: int, j: int) -> Iterator[tuple[int, int, T]]:
        for d in [-1, 1]:
            for di, dj in [[d, 0], [0, d]]:
                if (di == 0 and dj == 0) or not self.is_inside(i + di, j + dj):
                    continue
                yield i + di, j + dj, self[i + di, j + dj]

    def get_diagonal_neighbors(self, i: int, j: int) -> Iterator[tuple[int, int, T]]:
        for di, dj in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if (di == 0 and dj == 0) or not self.is_inside(i + di, j + dj):
                continue
            yield i + di, j + dj, self[i + di, j + dj]

    def is_inside(self, i: int, j: int) -> bool:
        return (0 <= i < self.n) and (0 <= j < self.m)

    def get(self, i: int, j: int, default: S) -> S | T:
        if not self.is_inside(i, j):
            return default
        return self[i, j]

    def safe_set(self, i: int, j: int, val: T) -> None:
        if not self.is_inside(i, j):
            return
        self[i, j] = val

    def to_graph(
        self,
        diagonal: bool,
        is_connected: Callable[[int, int, int, int], bool] | None = None,
    ) -> list[ExplicitNode]:
        graph: list[ExplicitNode] = []
        for i in range(self.n):
            for j in range(self.m):
                graph.append(ExplicitNode(i * self.m + j, graph, info=(i, j)))
        it_fn = self.get_diagonal_neighbors if diagonal else self.get_neighbors
        for i in range(self.n):
            for j in range(self.n):
                node = graph[i * self.m + j]
                for i1, j1, _ in it_fn(i, j):
                    if is_connected is not None and not is_connected(i, j, i1, j1):
                        continue
                    node.add_arrow(i1 * self.m + j1)
        return graph

    def __iter__(self) -> Iterator[tuple[int, int, T]]:
        for i in range(self.n):
            for j in range(self.m):
                yield i, j, self[i, j]
