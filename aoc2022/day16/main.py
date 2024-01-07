from typing import Iterator

from aoc_helper.graph import BaseNode
from aoc_helper.graph_distance import distance_from_topo
from aoc_helper.graph_traversal import bfs
from aoc_helper.graph_utils import to_explicit, topological_sort
from aoc_helper.utils import load_lines, timeit
from typing_extensions import Self


class SimpleNode(BaseNode):
    has_unique = True

    def __init__(
        self,
        rate: int,
        name: str,
        neighbors: list[str] | list[tuple[str, int]],
        every: dict[str, Self],
        idx: int,
    ):
        self.rate = rate
        self.name = name
        self.neighbors = [(n, 1) if isinstance(n, str) else n for n in neighbors]
        self.every = every
        self.every[name] = self
        self.idx = idx

    def unique(self) -> str:
        return self.name

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple[Self, int]]:
        assert not reverse, "Not implemented"
        for neighbor, distance in self.neighbors:
            yield self.every[neighbor], distance


class RiddleNode(BaseNode):
    has_unique = True

    def __init__(
        self,
        time_left: tuple[int, ...],
        pos: str,
        graph: dict[str, SimpleNode],
        opened: int,
    ):
        self.time_left = time_left
        self.pos = pos
        self.graph = graph
        self.opened = opened

    def unique(self) -> tuple[int, ...]:
        return (self.opened, self.graph[self.pos].idx, *self.time_left)

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["RiddleNode", int]]:
        time_idx, time_left = min(
            (k, val) for k, val in enumerate(self.time_left) if val > 0
        )
        assert not reverse, "Not implemented"
        for node, distance in self.graph[self.pos].get_weighted_neighbors():
            # distance + (open valve time) + (time for open valve to take effect)
            if (distance + 2) >= time_left or (self.opened & (1 << node.idx)):
                continue

            remaining_time = time_left - distance - 1
            new_time_left = (
                self.time_left[:time_idx]
                + (remaining_time,)
                + self.time_left[time_idx + 1 :]
            )
            yield RiddleNode(
                new_time_left,
                node.name,
                self.graph,
                self.opened | (1 << node.idx),
            ), -node.rate * remaining_time

        if time_idx == len(self.time_left) - 1:
            yield FinalNode(len(self.time_left)), 0
        else:
            new_time_left = (
                self.time_left[:time_idx] + (0,) + self.time_left[time_idx + 1 :]
            )
            yield RiddleNode(new_time_left, "start", self.graph, self.opened), 0


class FinalNode(RiddleNode):
    def __init__(self, num_times):
        self.time_left = tuple([0] * num_times)

    def unique(self) -> tuple[int, ...]:
        return (-2, -2, *self.time_left)

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["RiddleNode", int]]:
        assert not reverse, "Not implemented"
        yield from ()


@timeit
def process_data(filename: str):
    lines = load_lines(filename)

    all_nodes = dict()
    for k, line in enumerate(lines):
        words = line.replace(",", "").split(" ")
        name = words[1]
        rate = int(words[4][5:-1])
        neighbors = words[9:]
        all_nodes[name] = SimpleNode(rate, name, neighbors, all_nodes, k)

    flow_nodes = dict()
    k = 0
    for name, node in all_nodes.items():
        if node.rate == 0 and name != "AA":
            continue

        neighbors: list[tuple[str, int]] = []
        for neighbor, _, distance in bfs(node):
            if neighbor.rate == 0:
                continue

            neighbors.append((neighbor.name, distance))
        if node.rate > 0:
            flow_nodes[name] = SimpleNode(node.rate, name, neighbors, flow_nodes, k)
            k += 1
        if name == "AA":
            if node.rate > 0:
                neighbors.append(("AA", 0))
            flow_nodes["start"] = SimpleNode(0, "start", neighbors, flow_nodes, k)
            k += 1

    return flow_nodes


@timeit
def task1(flow_nodes: dict[str, SimpleNode]):
    beginning = RiddleNode((30,), "start", flow_nodes, 0)
    final = FinalNode(1)

    # upper bound for number of nodes here is
    # 2^(num flow nodes) * num flow nodes * num time steps
    # 2^15 * 15 * 30 approx 10^7
    # in praxis many of these states are not reachable -> much smaller search
    # space, in this case ~50,000 nodes
    all_riddlenodes, node_to_idx = to_explicit(beginning)

    # want to do a topological sort next, because of the strict time based
    # graph that we have here, we can simply sort by time instead and get
    # a topological sort by default. Saves a small amount of time.
    sorted_keys = list(node_to_idx.keys())
    sorted_keys.sort(key=lambda tpl: -tpl[-1])
    topo = [all_riddlenodes[node_to_idx[k]] for k in sorted_keys]
    # general topological_sort:
    # topo = topological_sort(all_riddlenodes)

    start_node = all_riddlenodes[node_to_idx[beginning.unique()]]
    end_node = all_riddlenodes[node_to_idx[final.unique()]]
    _, distances = distance_from_topo(start_node, topo)
    for node, distance in zip(topo, distances):
        if node == end_node:
            return -distance
    return -1


@timeit
def task2(flow_nodes: dict[str, SimpleNode]):
    beginning = RiddleNode((26, 26), "start", flow_nodes, 0)
    final = FinalNode(2)

    # number of nodes is higher here: 1,700,000
    all_riddlenodes, node_to_idx = to_explicit(beginning)

    # want to do a topological sort next, because of the strict time based
    # graph that we have here, we can simply sort by time instead and get
    # a topological sort by default. Saves a small amount of time.
    sorted_keys = list(node_to_idx.keys())
    sorted_keys.sort(key=lambda tpl: (-tpl[2], -tpl[3]))
    topo = [all_riddlenodes[node_to_idx[k]] for k in sorted_keys]
    # general topological_sort:
    # topo = topological_sort(all_riddlenodes)

    start_node = all_riddlenodes[node_to_idx[beginning.unique()]]
    end_node = all_riddlenodes[node_to_idx[final.unique()]]
    _, distances = distance_from_topo(start_node, topo)
    for node, distance in zip(topo, distances):
        if node == end_node:
            return -distance
    return -1


@timeit
def main(filename: str):
    data = process_data(filename)
    result1 = task1(data)
    result2 = task2(data)

    print(f"Task 1: {result1}")
    print(f"Task 2: {result2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
