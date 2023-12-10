from __future__ import annotations

import heapq
from abc import abstractmethod
from collections import deque
from collections.abc import Callable, Iterator
from itertools import count
from typing import Any, Generic, Optional, Protocol, Self, TypeVar

from .graph import BaseNode, Weight

__all__ = ["bfs", "dfs", "dijkstra", "a_star", "double_sided_distance"]
W = TypeVar("W", bound=Weight)  # weight for a weighted graph


def bfs(
    start: BaseNode | list[BaseNode], reversed: bool = False
) -> Iterator[tuple[BaseNode, int]]:
    """Breadth-first search"""
    if not isinstance(start, list):
        start = [start]

    # pyright assumes second argument is of type Literal[0] if not
    # specified, should be obvious ...
    queue: deque[tuple[BaseNode, int]] = deque((s, 0) for s in start)
    waiting = set(s for s in start)

    while len(queue) > 0:
        node, d = queue.popleft()
        yield node, d
        for neighbor in node.get_neighbors(reverse=reversed):
            if neighbor in waiting:
                continue

            queue.append((neighbor, d + 1))
            waiting.add(neighbor)


def dfs(start: BaseNode | list[BaseNode], reversed: bool = False) -> Iterator[BaseNode]:
    """Depth-first search"""
    if not isinstance(start, list):
        start = [start]

    stack = start
    visited = set()
    while len(stack) > 0:
        node = stack.pop()
        if node in visited:
            continue
        yield node
        visited.add(node)

        for neighbor in node.get_neighbors(reverse=reversed):
            if neighbor in visited:
                continue
            stack.append(neighbor)


def dijkstra(
    start: BaseNode[W] | list[BaseNode[W]],
    reversed: bool = False,
    start_weight: W = 0,  # pyright: ignore
) -> Iterator[tuple[BaseNode[W], W]]:
    """Dijkstra search algorithm for shortest path"""
    if not isinstance(start, list):
        start = [start]

    __counter = count()
    tiebreaker = lambda n: next(__counter)

    heap: list[tuple[W, int, BaseNode[W]]] = [
        (start_weight, tiebreaker(s), s) for s in start
    ]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        d, _, node = heapq.heappop(heap)
        if node in visited:
            continue
        yield node, d
        visited.add(node)
        for neighbor, w in node.get_weighted_neighbors(reverse=reversed):
            if neighbor not in visited:
                heapq.heappush(heap, (d + w, tiebreaker(neighbor), neighbor))


def a_star(
    start: BaseNode[W] | list[BaseNode[W]],
    heuristic: Callable[[BaseNode[W]], W],
    reversed: bool = False,
    start_weight: W = 0,  # pyright: ignore
) -> Iterator[tuple[BaseNode[W], W]]:
    """A start search algorithm for shortest path"""
    if not isinstance(start, list):
        start = [start]

    __counter = count()
    tiebreaker = lambda n: next(__counter)

    heap: list[tuple[W, W, int, BaseNode[W]]] = [
        (start_weight + heuristic(s), start_weight, tiebreaker(s), s) for s in start
    ]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        _, d, _, node = heapq.heappop(heap)
        if node in visited:
            continue
        yield node, d
        visited.add(node)
        for neighbor, w in node.get_weighted_neighbors(reverse=reversed):
            if neighbor in visited:
                continue
            tpl = (
                d + w + heuristic(neighbor),
                d + w,
                tiebreaker(neighbor),
                neighbor,
            )
            heapq.heappush(heap, tpl)


class WeightedTraversal(Protocol):
    @abstractmethod
    def __call__(
        self, start: BaseNode[W] | list[BaseNode], reversed: bool, start_weight: W
    ) -> Iterator[tuple[BaseNode[W], W]]:
        pass


def double_sided_distance(
    traversal: WeightedTraversal,
    start: BaseNode[W] | list[BaseNode[W]],
    end: BaseNode[W] | list[BaseNode[W]],
    start_weight: W = 0,  # pyright: ignore
    end_weight: W = 0,  # pyright: ignore
):
    # only returns shortest path, no intermediated traversal
    visited_forward: dict[BaseNode[W], W] = dict()
    visited_backward: dict[BaseNode[W], W] = dict()
    it_forward = traversal(start, reversed=False, start_weight=start_weight)
    it_backward = traversal(end, reversed=True, start_weight=start_weight)

    node_f, weight_f = next(it_forward)
    node_b, weight_b = next(it_backward)
    node = None
    try:
        while not (node in visited_forward and node in visited_backward):
            if weight_f <= weight_b:
                node = node_f
                visited_forward[node_f] = weight_f
                node_f, weight_f = next(it_forward)
            else:
                node = node_b
                visited_backward[node_b] = weight_b
                node_b, weight_b = next(it_backward)
    except StopIteration:
        raise ValueError("Given nodes have no connection")
    return visited_forward[node] + visited_backward[node]
