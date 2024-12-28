import itertools
import operator
from collections import deque
from typing import Callable, Hashable

from aoc_helper.graph import ExplicitKeyNode, dfs
from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


class WireNode(ExplicitKeyNode):
    all_nodes: dict[Hashable, "WireNode"]
    idx: str
    info: str | bool
    evaluated: bool | None
    operators = {"and": operator.and_, "or": operator.or_, "xor": operator.xor}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_waiting = False
        self.evaluated = None
        self.translated = None

    def get(self) -> bool:
        if isinstance(self.info, bool):
            return self.info
        elif self.evaluated is not None:
            return self.evaluated

        assert len(self.incoming) == 2 and isinstance(self.info, str)
        self.is_waiting = True

        (a_idx, _), (b_idx, _) = self.incoming
        a_node, b_node = self.all_nodes[a_idx], self.all_nodes[b_idx]
        assert not a_node.is_waiting
        a_val = a_node.get()
        assert not b_node.is_waiting
        b_val = b_node.get()
        self.is_waiting = False
        self.evaluated = self.operators[self.info](a_val, b_val)
        return self.evaluated

    def reset(self):
        if isinstance(self.info, bool) or self.evaluated is None:
            return

        self.evaluated = None
        for node_idx, _ in self.incoming:
            self.all_nodes[node_idx].reset()

    def translate(self) -> tuple[str, int]:
        # names
        # raw_k: x_k XOR y_k
        # direct_k: x_k AND y_k
        # carry_k: carry of op k-1
        # -> z_k = raw_k XOR carry_k
        # -> carry_(k+1) = (x_k AND y_k) OR (x_k AND carry_k) OR (y_k AND carry_k)
        #                = (x_k AND y_k) OR ((x_k OR y_k) AND carry_k)
        #                = (x_k AND y_k) OR (raw_k AND carry_k)
        #                = direct_k OR sub_carry_(k+1)
        # sub_carry_(k+1) = raw_k AND carry_k
        if self.translated is not None:
            return self.translated

        if self.idx[0] == "x" or self.idx[0] == "y":
            self.translated = (self.idx[0], int(self.idx[1:]))
        else:

            (a_idx, _), (b_idx, _) = self.incoming
            a_node, b_node = self.all_nodes[a_idx], self.all_nodes[b_idx]
            a_trans = a_node.translate()
            b_trans = b_node.translate()
            if a_trans > b_trans:
                a_idx, a_node, a_trans, b_idx, b_node, b_trans = (
                    b_idx,
                    b_node,
                    b_trans,
                    a_idx,
                    a_idx,
                    a_trans,
                )
            if a_trans[0] == "unk" or b_trans[0] == "unk":
                self.translated = ("unk", -1)
            else:
                if a_trans[0] == "x" and b_trans[0] == "y" and a_trans[1] == b_trans[1]:
                    if self.info == "xor":
                        self.translated = ("raw", a_trans[1])
                    elif self.info == "and":
                        self.translated = ("direct", a_trans[1])
                    else:
                        self.translated = ("unk", -1)
                elif (
                    a_trans[0] == "carry"
                    and b_trans[0] == "raw"
                    and a_trans[1] == b_trans[1]
                ) or (a_trans == ("direct", 0) and b_trans == ("raw", 1)):
                    if self.info == "xor":
                        self.translated = ("z", b_trans[1])
                    elif self.info == "and":
                        self.translated = ("sub_carry", b_trans[1] + 1)
                    else:
                        self.translated = ("unk", -1)
                elif (
                    a_trans[0] == "direct"
                    and b_trans[0] == "sub_carry"
                    and a_trans[1] + 1 == b_trans[1]
                    and self.info == "or"
                ):
                    self.translated = ("carry", b_trans[1])
                else:
                    self.translated = ("unk", -1)

        for node in self.get_neighbors():
            node.translate()

        return self.translated

    def reset_translate(self):
        self.translated = None
        for node in self.get_neighbors():
            node.reset_translate()

    def __repr__(self) -> str:
        return (
            f"WireNode({self.idx}, {self.info}, "
            f"{[node.idx for node in self.get_neighbors(reverse=True)]})"
        )

    def __str__(
        self, indent_level: int = 0, rename_dict: dict[str, str] | None = None
    ) -> str:
        whitespace = "  "
        if isinstance(self.info, bool):
            return ""
            # return whitespace * indent_level + f"{self.idx}: const {self.info}\n"

        rename_dict = {} if rename_dict is None else rename_dict
        (a_idx, _), (b_idx, _) = self.incoming
        if self.translated is not None and self.translated[0] != "unk":
            info = whitespace * indent_level + f"{self.idx}: {self.translated}\n"
        else:
            info = (
                whitespace * indent_level + f"{self.idx}: {a_idx} {self.info} {b_idx}\n"
            )
            if a_idx in rename_dict:
                info += (
                    whitespace * (indent_level + 1) + f"{a_idx}: {rename_dict[a_idx]}\n"
                )
            else:
                info += self.all_nodes[a_idx].__str__(indent_level + 1, rename_dict)
            if b_idx in rename_dict:
                info += (
                    whitespace * (indent_level + 1) + f"{b_idx}: {rename_dict[b_idx]}\n"
                )
            else:
                info += self.all_nodes[b_idx].__str__(indent_level + 1, rename_dict)
        return info[: len(info) - (indent_level == 0)]


@timeit
def prepare_input(lines: list[str]) -> tuple[dict[str, WireNode]]:
    graph: dict[str, WireNode] = dict()
    fifo = deque(lines)
    while len(fifo) > 0:
        line = fifo.popleft()
        if line == "":
            continue
        elif ":" in line:
            name, val = line.split(": ")
            graph[name] = WireNode(name, graph, bool(int(val)))
        else:
            name_a, op, name_b, _, name_out = line.split()
            if name_a not in graph or name_b not in graph:
                fifo.append(line)
                continue
            graph[name_out] = WireNode(name_out, graph, op.lower())
            node_a, node_b = graph[name_a], graph[name_b]
            node_a.add_arrow(name_out)
            node_b.add_arrow(name_out)
    return (graph,)


@timeit
def task1(graph: dict[str, WireNode]) -> int:
    result = 0
    for name, node in graph.items():
        if not name.startswith("z"):
            continue
        idx = int(name[1:])
        val = node.get()
        result += val << idx
    return result


def swap_wires(
    graph: dict[str, WireNode],
    idx_a: str,
    idx_b: str,
    zs: list[WireNode],
    swaps: list[str],
):
    swaps.append(idx_a)
    swaps.append(idx_b)
    node_a, node_b = graph[idx_a], graph[idx_b]
    node_a.outgoing, node_b.outgoing = node_b.outgoing, node_a.outgoing
    node_a.outgoing_set, node_b.outgoing_set = node_b.outgoing_set, node_a.outgoing_set
    for other in node_a.get_neighbors():
        other.incoming_set.remove(idx_b)
        other.incoming_set.add(idx_a)
        for k in range(len(other.incoming)):
            if other.incoming[k][0] == idx_b:
                other.incoming[k] = (idx_a, other.incoming[k][1])
    for other in node_b.get_neighbors():
        other.incoming_set.remove(idx_a)
        other.incoming_set.add(idx_b)
        for k in range(len(other.incoming)):
            if other.incoming[k][0] == idx_a:
                other.incoming[k] = (idx_b, other.incoming[k][1])

    if idx_a[0] == "z":
        loc_a = int(idx_a[1:])
        zs[loc_a] = node_b

    if idx_b[0] == "z":
        loc_b = int(idx_b[1:])
        zs[loc_b] = node_a

    node_a.reset_translate()
    node_b.reset_translate()
    node_a.translate()
    node_b.translate()


@timeit
def task2(graph: dict[str, WireNode]) -> str:
    """
    A semi-automatic solution for part 2. To solve, translate the graph,
    manually inspect the nodes that cause the error and determine which wires
    need to be swapped.
    """
    all_swaps = []

    x = [node for name, node in graph.items() if name[0] == "x"]
    x_set = set(x)
    x.sort(key=lambda n: n.idx)
    y = [node for name, node in graph.items() if name[0] == "y"]
    y.sort(key=lambda n: n.idx)
    y_set = set(y)
    z = [node for name, node in graph.items() if name[0] == "z"]
    z.sort(key=lambda n: n.idx)

    # check that z[k] depends only on x[:k], y[:k]
    for k in range(len(z)):
        childs = {node for node, _ in dfs(z[:k], reversed=True)}
        if childs & x_set != set(x[:k]):
            print(f"x{k} wrongly wired", {c.idx for c in childs & x_set})
            raise ValueError("Failed to solve")
        if childs & y_set != set(y[:k]):
            print(f"y{k} wrongly wired", {c.idx for c in childs & y_set})
            raise ValueError("Failed to solve")
    # -> worked without changing any wires for me, will need some swapping
    # based on this, if it breaks

    x[-1].translate()
    for _ in range(4):
        k = 0
        while k < len(z) and (
            z[k].translated == ("z", k) or z[k].translated == ("raw", 0)
        ):
            k += 1
        if k >= len(z) - 1:
            raise ValueError("Failed to solve")

        # wrongly wired gates need to be correct gates that are not recognized
        # in their current location, i.e. ancestor nodes of unkown nodes.
        unkown_nodes = []
        for node, _ in dfs([z[k], z[k + 1]], reversed=True):
            if node.translate()[0] == "unk":
                unkown_nodes.append(node)
        candidate_nodes = [
            prev
            for node in unkown_nodes
            for prev in node.get_neighbors(reverse=True)
            if prev.translate()[0] != "unk"
        ]

        # if we find a node that contains (z, k) that is sufficient to know a
        # swap, since (z, k) allways needs to be f"z{k:02}".
        direct_z_swap = [
            node for node in candidate_nodes if node.translate() == ("z", k)
        ]
        if len(direct_z_swap) == 1:
            node_a, node_b = z[k], direct_z_swap[0]
            print(f"Swapping {node_a.idx} and {node_b.idx}")
            swap_wires(graph, node_a.idx, node_b.idx, z, all_swaps)
            continue

        # try all possible swaps
        solved = False
        for k, node_a in enumerate(candidate_nodes):
            for node_b in candidate_nodes[k + 1 :]:
                swap_wires(graph, node_a.idx, node_b.idx, z, [])
                if z[k].translate() == ("z", k):
                    print(f"Swapping {node_a.idx} and {node_b.idx}")
                    all_swaps.append(node_a.idx)
                    all_swaps.append(node_b.idx)
                    solved = True
                    break
                else:
                    swap_wires(graph, node_a.idx, node_b.idx, z, [])
            if solved:
                break

        if not solved:
            raise ValueError("Failed to solve")

    # check that our swaps were actually sucessfull
    for k in range(1, len(z) - 1):
        if z[k].translate() != ("z", k):
            raise ValueError("Failed to solve")
    if z[0].translate() != ("raw", 0) or z[-1].translate() != ("carry", len(z) - 1):
            raise ValueError("Failed to solve")

    return ",".join(sorted(all_swaps))


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
