from collections import defaultdict

from aoc_helper.graph.base import ExplicitKeyNode
from aoc_helper.utils import ExclusiveTimeIt, load_lines

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> dict[str, ExplicitKeyNode]:
    graph = dict()
    for line in lines:
        name, connections = line.split(": ")
        graph[name] = ExplicitKeyNode(name, graph)
    if "out" not in graph:
        graph["out"] = ExplicitKeyNode("out", graph)
    for line in lines:
        name, connections = line.split(": ")
        node = graph[name]
        for other in connections.split(" "):
            node.add_arrow(other)
    return graph


def topological_sort(nodes: dict[str, ExplicitKeyNode]) -> list[str]:
    # kahn's algorithm
    topo: list[str] = []

    # create a copy to delete edges
    start_nodes: list[str] = []
    num_marked_edges = defaultdict(int)
    for node in nodes.values():
        if len(node.incoming) == 0:
            start_nodes.append(node.idx)

    if len(start_nodes) == 0:
        raise ValueError("Graph contains cycle")

    while len(start_nodes) > 0:
        current = start_nodes.pop()
        topo.append(current)
        for neighbor in nodes[current].get_neighbors():
            num_marked_edges[neighbor.idx] += 1
            if len(neighbor.incoming) == num_marked_edges[neighbor.idx]:
                start_nodes.append(neighbor.idx)

    if len(topo) < len(nodes):
        raise ValueError(
            f"Graph isn't acyclic, can't sort. {len(topo)} from {len(nodes)} sorted."
        )

    return topo


@timeit
def task1(graph: dict[str, ExplicitKeyNode]) -> int:
    ordered = topological_sort(graph)
    num_paths = defaultdict(int)
    num_paths["you"] = 1
    for name in ordered:
        for other in graph[name].get_neighbors():
            num_paths[other.idx] += num_paths[name]
    return num_paths["out"]


@timeit
def task2(graph: dict[str, ExplicitKeyNode]) -> int:
    ordered = topological_sort(graph)

    # forced order of dac and fft
    idx_dac = ordered.index("dac")
    idx_fft = ordered.index("fft")
    name_first = "fft" if idx_fft < idx_dac else "dac"
    name_second = "fft" if idx_fft >= idx_dac else "dac"

    stops = ["svr", name_first, name_second, "out"]
    stop_idx = [ordered.index(name) for name in stops]
    stops_counts = [1]

    for k in range(len(stops) - 1):
        num_paths = defaultdict(int)
        num_paths[stops[k]] = stops_counts[-1]
        for name in ordered[stop_idx[k] : stop_idx[k + 1]]:
            for other in graph[name].get_neighbors():
                num_paths[other.idx] += num_paths[name]
        stops_counts.append(num_paths[stops[k + 1]])

    return stops_counts[-1]


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
