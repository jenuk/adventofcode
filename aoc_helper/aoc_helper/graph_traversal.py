from __future__ import annotations

import heapq
from abc import abstractmethod
from collections import deque
from collections.abc import Callable, Iterator
from itertools import count
from typing import Protocol, TypeVar

from .graph import BaseNode, Weight

__all__ = ["bfs", "dfs", "dijkstra", "a_star", "double_sided_distance"]
W = TypeVar("W", bound=Weight)  # weight for a weighted graph
Node = TypeVar("Node", bound=BaseNode)


def bfs(start: Node | list[Node], reversed: bool = False) -> Iterator[tuple[Node, int]]:
    """Breadth-first search"""
    if not isinstance(start, list):
        start = [start]

    # pyright assumes second argument is of type Literal[0] if not
    # specified, should be obvious ...
    queue: deque[tuple[Node, int]] = deque((s, 0) for s in start)
    waiting = set(s for s in start)

    while len(queue) > 0:
        node, d = queue.popleft()
        yield node, d
        for neighbor in node.get_neighbors(reverse=reversed):
            if neighbor in waiting:
                continue

            queue.append((neighbor, d + 1))
            waiting.add(neighbor)


def dfs(start: Node | list[Node], reversed: bool = False) -> Iterator[Node]:
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
    start: Node | list[Node],
    reversed: bool = False,
    start_weight: W = 0,  # pyright: ignore
) -> Iterator[tuple[Node, Node, W]]:
    """Dijkstra search algorithm for shortest path"""
    if not isinstance(start, list):
        start = [start]

    __counter = count()
    tiebreaker = lambda n: next(__counter)

    heap: list[tuple[W, int, Node, Node]] = [
        (start_weight, tiebreaker(s), s, s) for s in start
    ]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        d, _, node, parent = heapq.heappop(heap)
        if node in visited:
            continue
        yield node, parent, d
        visited.add(node)
        for neighbor, w in node.get_weighted_neighbors(reverse=reversed):
            if neighbor not in visited:
                heapq.heappush(heap, (d + w, tiebreaker(neighbor), neighbor, node))


def a_star(
    start: Node | list[Node],
    heuristic: Callable[[Node], W],
    reversed: bool = False,
    start_weight: W = 0,  # pyright: ignore
) -> Iterator[tuple[Node, W]]:
    """A start search algorithm for shortest path"""
    if not isinstance(start, list):
        start = [start]

    __counter = count()
    tiebreaker = lambda n: next(__counter)

    heap: list[tuple[W, W, int, Node]] = [
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
        self, start: Node | list[Node], reversed: bool, start_weight: W
    ) -> Iterator[tuple[Node, W]]:
        pass


def double_sided_distance(
    traversal: WeightedTraversal,
    start: Node | list[Node],
    end: Node | list[Node],
    start_weight: W = 0,  # pyright: ignore
    end_weight: W = 0,  # pyright: ignore
):
    # only returns shortest path, no intermediated traversal
    visited_forward: dict[Node, W] = dict()
    visited_backward: dict[Node, W] = dict()
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
