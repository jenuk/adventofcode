import operator
import dataclasses
from typing import Hashable, Iterator

from aoc_helper.graph import BaseNode
from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.graph_traversal import dfs

timeit = ExclusiveTimeIt()


@dataclasses.dataclass
class NodeStatus:
    target: int
    operands: list[int]
    pos: int
    value: int


class LineNode(BaseNode):
    has_unique = True  # compare only via `self.unique() == other.unique()`
    operators = {"add": operator.add, "mul": operator.mul}

    def __init__(self, status: NodeStatus):
        self.status = status

    def unique(self) -> Hashable:
        return (self.status.pos, self.status.value)

    def get_neighbors(self, reverse: bool = False) -> Iterator["LineNode"]:
        if reverse:
            if self.status.pos == 0:
                return
            for op in LineNode.operators.keys():
                x = self.status.value
                y = self.status.operands[self.status.pos]
                if op == "add":
                    new_value = x - y
                elif op == "mul":
                    if x % y != 0:
                        continue
                    new_value = x // y
                elif op == "cat":
                    if x == y or not str(x).endswith(str(y)):
                        continue
                    new_value = int(str(x)[: -len(str(y))])
                else:
                    raise ValueError(f"Unknown operation {op}")
                new_status = dataclasses.replace(
                    self.status, pos=self.status.pos - 1, value=new_value
                )
                yield LineNode(new_status)
        else:
            if self.status.pos == len(self.status.operands) - 1:
                return
            for fn in LineNode.operators.values():
                new_value = fn(
                    self.status.value, self.status.operands[self.status.pos + 1]
                )
                if new_value <= self.status.target:
                    new_status = dataclasses.replace(
                        self.status, pos=self.status.pos + 1, value=new_value
                    )
                    yield LineNode(new_status)


@timeit
def prepare_input(lines: list[str]):
    new_lines = []
    for line in lines:
        target, vals = line.split(":")
        new_lines.append((int(target), list(map(int, vals.strip().split()))))

    return new_lines


@timeit
def task1(lines: list[tuple[int, list[int]]]) -> tuple[int, list[bool]]:
    result = 0
    solved = [False] * len(lines)
    for k, (target, vals) in enumerate(lines):
        start = LineNode(
            NodeStatus(
                target=target,
                operands=vals,
                pos=0,
                value=vals[0],
            )
        )
        end = LineNode(
            NodeStatus(
                target=target,
                operands=vals,
                pos=len(vals) - 1,
                value=target,
            )
        )
        start_unique = start.unique()

        # can also do `dfs(start, reversed=False)` and `other_node == end`
        for other_node, _ in dfs(end, reversed=True):
            if other_node.unique() == start_unique:
                solved[k] = True
                result += target
                break
    return result, solved


@timeit
def task2(lines: list[tuple[int, list[int]]]) -> int:
    result1, solved = task1(lines)
    LineNode.operators["cat"] = lambda x, y: int(str(x) + str(y))
    result2, _ = task1([line for k, line in enumerate(lines) if not solved[k]])
    del LineNode.operators["cat"]
    return result1 + result2


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1, _ = task1(inp)
    total_p2 = task2(inp)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
