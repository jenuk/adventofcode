from aoc_helper.graph import ExplicitNode
from aoc_helper.graph_utils import to_explicit, topological_sort
from aoc_helper.utils import load_lines, timeit


@timeit
def prepare_input(lines: str):
    idx = lines.index("")
    rules, updates = lines[:idx], lines[idx + 1 :]

    rules = [(int((t := r.split("|"))[0]), int(t[1])) for r in rules]
    updates = [list(map(int, line.split(","))) for line in updates]

    max_node = max(max(map(max, rules)), max(map(max, updates)))
    nodes: list[ExplicitNode] = []
    for k in range(max_node + 1):
        nodes.append(ExplicitNode(k, nodes))

    for left, right in rules:
        nodes[left].add_arrow(right)

    return nodes, updates


@timeit
def task1(
    nodes: list[ExplicitNode], updates: list[list[int]]
) -> tuple[int, list[bool]]:
    result = 0
    solved = []
    for line in updates:
        previous = []
        failed = False
        for page in line:
            for prev_page in previous:
                if prev_page in nodes[page].outgoing_set:
                    failed = True
                    break
            if failed:
                break
            previous.append(page)
        solved.append(not failed)
        if failed:
            continue
        result += line[len(line) // 2]

    return result, solved


@timeit
def task2(
    nodes: list[ExplicitNode], updates: list[list[int]], solved: list[bool]
) -> int:
    result = 0
    for solve, line in zip(solved, updates):
        if solve:
            continue

        # make a subgraph
        complete_line, _ = to_explicit([nodes[idx] for idx in line], strict_nodes=True)

        try:
            sorted = topological_sort(complete_line)
        except ValueError as e:
            print(f"{line=} is unsorteable '{e}'")
            continue
        result += sorted[len(sorted) // 2].info.idx
    return result


def main(fn: str):
    lines = load_lines(fn)
    nodes, updates = prepare_input(lines)

    total_p1, solved = task1(nodes, updates)
    total_p2 = task2(nodes, updates, solved)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
