import copy
import heapq

from aoc_helper.select import quickselect
from aoc_helper.utils import ExclusiveTimeIt, load_lines

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    nodes = [tuple(map(int, line.split(","))) for line in lines]
    edges = []
    for i in range(len(nodes)):
        for j in range(i):
            a = nodes[i]
            b = nodes[j]
            d = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
            edges.append((d, i, j))
    return nodes, edges


def get_component(components: list[int], start: int) -> int:
    current = start
    while components[current] != current:
        current = components[current]
    while components[start] != current:
        start, components[start] = components[start], current
    return current


@timeit
def task1(
    nodes: list[tuple[int, int, int]],
    edges: list[tuple[int, int, int]],
    num_joints: int = 1000,
) -> int:
    heap = copy.copy(edges)
    quickselect(heap, num_joints)
    components = list(range(len(nodes)))
    components_count = [1] * len(nodes)
    for i in range(num_joints):
        _, a, b = heap[i]
        a_component = get_component(components, a)
        b_component = get_component(components, b)
        if a_component == b_component:
            continue

        components[b_component] = a_component
        components_count[a_component] += components_count[b_component]
        components_count[b_component] = 0

    largerst = heapq.nlargest(3, components_count)
    result = largerst[0] * largerst[1] * largerst[2]

    return result


@timeit
def task2(
    nodes: list[tuple[int, int, int]],
    edges: list[tuple[int, int, int]],
) -> int:
    result = 0
    heap = copy.copy(edges)
    heapq.heapify(heap)
    components = list(range(len(nodes)))
    num_components = len(nodes)
    last_pair = None
    while num_components > 1:
        _, a, b = heapq.heappop(heap)
        a_component = get_component(components, a)
        b_component = get_component(components, b)
        components[b_component] = a_component
        num_components -= a_component != b_component
        last_pair = (a, b)

    assert last_pair is not None
    result = nodes[last_pair[0]][0] * nodes[last_pair[1]][0]
    return result


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
