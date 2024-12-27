from collections import deque
from typing import Hashable, TypeVar

from .base import BaseNode, ExplicitNode, Weight

W = TypeVar("W", bound=Weight)  # weight for a weighted graph
Node = TypeVar("Node", bound=BaseNode)


def to_explicit(
    nodes: Node | list[Node],
    strict_nodes: bool = False,
) -> tuple[list[ExplicitNode], dict[Hashable, int]]:
    if not isinstance(nodes, list):
        nodes = [nodes]

    # need to copy here, since I need to see all edges
    queue: deque[tuple[Node, int]] = deque((s, 0) for s in nodes)
    if nodes[0].has_unique:
        uniq = lambda n: n.unique()
    else:
        uniq = lambda n: n
    node_to_idx: dict[Hashable, int] = {}
    explicit_nodes: list[ExplicitNode] = []
    for k, node in enumerate(nodes):
        explicit_nodes.append(ExplicitNode(k, explicit_nodes, info=node))
        node_to_idx[uniq(node)] = k

    while len(queue) > 0:
        node, d = queue.popleft()
        for neighbor, distance in node.get_weighted_neighbors():
            if uniq(neighbor) not in node_to_idx:
                if strict_nodes:
                    continue
                queue.append((neighbor, d + distance))
                node_to_idx[uniq(neighbor)] = len(explicit_nodes)
                explicit_nodes.append(
                    ExplicitNode(len(explicit_nodes), explicit_nodes, info=neighbor)
                )
            explicit_nodes[node_to_idx[uniq(node)]].add_arrow(
                node_to_idx[uniq(neighbor)], distance
            )

    return explicit_nodes, node_to_idx


def topological_sort(nodes: list[ExplicitNode]) -> list[ExplicitNode]:
    # kahn's algorithm
    topo: list[ExplicitNode] = []

    # create a copy to delete edges
    start_nodes: list[ExplicitNode] = []
    num_marked_edges = [0] * len(nodes)
    for node in nodes:
        if len(node.incoming) == 0:
            start_nodes.append(node)

    if len(start_nodes) == 0:
        raise ValueError("Graph contains cycle")

    while len(start_nodes) > 0:
        current = start_nodes.pop()
        topo.append(current)
        for neighbor in current.get_neighbors():
            num_marked_edges[neighbor.idx] += 1
            if len(neighbor.incoming) == num_marked_edges[neighbor.idx]:
                start_nodes.append(neighbor)

    if len(topo) < len(nodes):
        raise ValueError(
            f"Graph isn't acyclic, can't sort. {len(topo)} from {len(nodes)} sorted."
        )

    return topo
