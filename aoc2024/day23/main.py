import itertools
from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.graph import ExplicitNode

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[list[ExplicitNode]]:
    graph = []
    name2loc: dict[str, tuple[int, ExplicitNode]] = dict()
    for line in lines:
        a, b = line.split("-")
        if a not in name2loc:
            graph.append(ExplicitNode(len(graph), graph, a))
            name2loc[a] = (len(graph) - 1, graph[-1])
        if b not in name2loc:
            graph.append(ExplicitNode(len(graph), graph, b))
            name2loc[b] = (len(graph) - 1, graph[-1])
        name2loc[a][1].add_arrow(name2loc[b][0])
        name2loc[b][1].add_arrow(name2loc[a][0])
    return (graph,)


@timeit
def task1(graph: list[ExplicitNode]) -> int:
    result = 0
    for node_a in graph:
        if node_a.info[0] != "t":
            continue

        for node_b_idx in node_a.incoming_set:
            node_b = graph[node_b_idx]
            if node_b.info[0] == "t" and (node_b_idx <= node_a.idx):
                continue

            for node_c_idx in node_a.incoming_set & node_b.incoming_set:
                if node_c_idx <= node_b_idx or (
                    graph[node_c_idx].info[0] == "t" and node_c_idx <= node_a.idx
                ):
                    continue
                result += 1
    return result


@timeit
def task2(graph: list[ExplicitNode]) -> str:
    maxium_length = 0
    maximum_clique = None
    # maximum clique problem is an np-equivalent problem, solved here via
    # enumeration. In general this will be slow.
    # This/my specific graph has 512 nodes and each has 13 edges -> at most
    # 512*2^13 (approx 4 mio) iterations, which can be solved <1s
    for base in graph:
        for choice in itertools.product(*([1, 0] for _ in range(len(base.incoming)))):
            if sum(choice) < maxium_length:
                continue

            clique = [
                graph[node_idx]
                for k, (node_idx, _) in enumerate(base.incoming)
                if choice[k]
            ]
            clique.append(base)
            shared_ids = set.intersection(
                *(node.incoming_set | {node.idx} for node in clique)
            )
            if shared_ids == set(node.idx for node in clique) and maxium_length < len(
                clique
            ):
                maxium_length = len(clique)
                maximum_clique = clique
    if maximum_clique is None:
        return ""

    return ",".join(sorted([node.info for node in maximum_clique]))


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
