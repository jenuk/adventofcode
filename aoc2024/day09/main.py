from typing import Iterable

from aoc_helper.linked_list import LinkedNode
from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> tuple[list[int], list[tuple[int, int]]]:
    line = [int(x) for x in lines[0]]
    blocks = []
    compact_line = []
    is_file = True
    file_id = 0
    for x in line:
        if x > 0:
            compact_line.append((file_id if is_file else -1, x))
            blocks.extend([file_id if is_file else -1] * x)
        file_id += is_file
        is_file = not is_file
    return blocks, compact_line


def calc_score(line: Iterable[int]) -> int:
    return sum(k * x for k, x in enumerate(line) if x != -1)


@timeit
def task1(line: list[int]) -> int:
    line = line[:]  # don't change the reference
    p_empty = 0
    p_full = len(line) - 1
    while p_empty < p_full:
        if line[p_empty] != -1:
            p_empty += 1
        elif line[p_full] == -1:
            p_full -= 1
        else:
            line[p_empty] = line[p_full]
            line[p_full] = -1
    return calc_score(line)


@timeit
def task2(line: list[tuple[int, int]]) -> int:
    start = None
    end = None
    for el in line:
        if end is None:
            start = LinkedNode(el)
            end = start
        else:
            end = end.insert(el)
    assert start is not None and end is not None

    for node_a in end.reversed():
        x, l = node_a.value
        if x == -1:
            continue

        for node_b in start:
            if node_a is node_b:
                break

            y, s = node_b.value
            if y != -1:
                continue
            elif s < l:
                continue

            node_b.value = (x, l)
            # we don't need to verify if we can simplify the compact
            # represention, e.g. merge adjacent empty blocks, here since
            # the start conditions guarantees that both adjacent blocks are
            # non-empty and the algorithm doesn't change it inside our search
            # range
            node_a.value = (-1, l)
            if l < s:
                # we don't need to merge here, since there might be empty
                # adjacent blocks here, but they are outside our search radius.
                # This is only updated for the score calulcation.
                node_b.insert((-1, s - l))
            break

    return calc_score(node.value[0] for node in start for _ in range(node.value[1]))


def main(fn: str):
    lines = load_lines(fn)
    inp_1, inp_2 = prepare_input(lines)

    total_p1 = task1(inp_1)
    total_p2 = task2(inp_2)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
