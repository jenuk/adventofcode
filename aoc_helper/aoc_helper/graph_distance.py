from typing import TypeVar
from .graph import BaseNode, Weight, ExplicitNode
from .graph_traversal import dijkstra

W = TypeVar("W", bound=Weight)  # weight for a weighted graph
Node = TypeVar("Node", bound=BaseNode)


def bellman_ford(
    start: Node, graph: list[Node], inf: W = float("inf"), check_cycles: bool = False
) -> tuple[list[Node], list[W]]:
    """Computes shortest paths between start node and all other nodes"""
    distances = [inf for _ in graph]
    parents = [n for n in graph]

    start_idx = graph.index(start)
    distances[start_idx] = 0

    # extract edge list from graph and cache
    edges = []
    for k, node in enumerate(graph):
        for neighbor, dist in node.get_weighted_neighbors():
            j = graph.index(neighbor)
            edges.append((k, j, dist))
            if k == start_idx:
                distances[j] = dist
                parents[j] = start

    for _ in range(len(graph) - (not check_cycles)):
        updated = False
        for n_in, n_out, w in edges:
            if distances[n_in] + w < distances[n_out]:
                parents[n_out] = graph[n_in]
                distances[n_out] = distances[n_in] + w
                updated = True
        if not updated:
            break
    else:
        if check_cycles:
            raise ValueError("Found negative cycle")

    return parents, distances


def dijkstra2(
    start: Node, graph: list[Node], inf: W = float("inf")
) -> tuple[list[Node], list[W]]:
    # same interface as bellman_ford
    distances = [inf for _ in graph]
    parents = [n for n in graph]

    start_idx = graph.index(start)
    distances[start_idx] = 0

    for node, parent, weight in dijkstra(start):
        node_idx = graph.index(node)
        distances[node_idx] = weight
        parents[node_idx] = parent

    return parents, distances


def floyd_warshall(
    graph: list[Node], inf: W = float("inf"), check_cycles: bool = False
) -> list[list[W]]:
    """Computes shortest paths between all nodes

    this implementation is not optimized for undirected graphs"""
    distances: list[list[W]] = [[inf for _ in graph] for _ in graph]

    # populate distance matrix with existing edges
    for k, node in enumerate(graph):
        for neighbor, dist in node.get_weighted_neighbors():
            distances[k][graph.index(neighbor)] = dist

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]

    if check_cycles:
        for i in range(len(graph)):
            if distances[i][i] < 0:
                raise ValueError("Found negative cycle")

    return distances


def aggregate_dijkstra(graph: list[Node], inf: W = float("inf")) -> list[list[W]]:
    # same interface as floyd_warshall
    distances = []

    for node in enumerate(graph):
        distances.append(dijkstra2(node, graph, inf=inf)[1])

    return distances


def distance_from_topo(
    start: ExplicitNode, graph: list[ExplicitNode], inf: W = float("inf")
) -> tuple[list[ExplicitNode], list[W]]:
    distances = [inf] * len(graph)
    parents = [n for n in graph]
    idx_to_pos = [-1] * len(graph)
    for k, node in enumerate(graph):
        idx_to_pos[node.idx] = k
    distances[idx_to_pos[start.idx]] = 0

    for k, node in enumerate(graph):
        for parent, distance in node.get_weighted_neighbors(reverse=True):
            parent_pos = idx_to_pos[parent.idx]
            if (total := distances[parent_pos] + distance) < distances[k]:
                distances[k] = total
                parents[k] = parent

    return parents, distances
