from collections import defaultdict
import heapq

from aoc_helper.graph.base import ExplicitNode
from aoc_helper.utils import ExclusiveTimeIt, load_lines
from aoc_helper.vector import euclidean

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> list[ExplicitNode]:
    graph = []
    for line in lines:
        loc = tuple(map(int, line.split(",")))
        node = ExplicitNode(len(graph), graph, loc)
        graph.append(node)

        for other in graph[:-1]:
            distance = euclidean(node.info, other.info)
            node.add_arrow(other.idx, distance)
            other.add_arrow(node.idx, distance)

    return graph


def get_component(components: dict[int, int], start: int) -> int:
    visited = [start]
    current = start
    while components[current] != current:
        current = components[current]
        visited.append(current)
    for v in visited:
        components[v] = current
    return current


@timeit
def task1(graph: list[ExplicitNode], num_joints: int = 1000) -> int:
    heap = [
        (dist, node.idx, neighbor.idx)
        for node in graph
        for neighbor, dist in node.get_weighted_neighbors()
        if node.idx < neighbor.idx
    ]
    heapq.heapify(heap)
    components = {node.idx: node.idx for node in graph}
    for _ in range(num_joints):
        _, a, b = heapq.heappop(heap)
        a_component = get_component(components, a)
        b_component = get_component(components, b)
        if a_component == b_component:
            continue
        components[b_component] = a_component

    component_count = defaultdict(int)
    for node in graph:
        component_count[get_component(components, node.idx)] += 1

    counts = list(component_count.values())
    counts.sort()
    result = counts[-3] * counts[-2] * counts[-1]

    return result


@timeit
def task2(graph: list[ExplicitNode]) -> int:
    result = 0
    heap = [
        (dist, node.idx, neighbor.idx)
        for node in graph
        for neighbor, dist in node.get_weighted_neighbors()
        if node.idx < neighbor.idx
    ]
    heapq.heapify(heap)
    components = {node.idx: node.idx for node in graph}
    num_components = len(graph)
    last_pair = None
    while num_components > 1:
        _, a, b = heapq.heappop(heap)
        a_component = get_component(components, a)
        b_component = get_component(components, b)
        if a_component == b_component:
            continue
        components[b_component] = a_component
        num_components -= 1
        last_pair = (a, b)

    assert last_pair is not None
    result = graph[last_pair[0]].info[0] * graph[last_pair[1]].info[0]
    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(inp)
    total_p2 = task2(inp)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
