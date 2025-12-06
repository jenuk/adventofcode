import operator
from functools import reduce

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> tuple[list[list[str]], list[str]]:
    split_idx = [
        k
        for k in range(len(lines[0]))
        if all(lines[i][k] == " " for i in range(len(lines)))
    ]
    split_idx.insert(0, -1)
    split_idx.append(len(lines[0]))
    matrix = []
    for line in lines[:-1]:
        line_split = [
            line[k1 + 1 : k2] for k1, k2 in zip(split_idx[:-1], split_idx[1:])
        ]
        matrix.append(line_split)
    ops = lines[-1].split()
    return matrix, ops


@timeit
def task1(matrix: list[list[str]], ops: list[str]) -> int:
    result = 0
    for i in range(len(ops)):
        op = operator.add if ops[i] == "+" else operator.mul
        start = 0 if ops[i] == "+" else 1
        result += reduce(op, (int(matrix[j][i]) for j in range(len(matrix))), start)
    return result


@timeit
def task2(matrix: list[list[str]], ops: list[str]) -> int:
    result = 0
    for i in range(len(ops)):
        block = [matrix[j][i] for j in range(len(matrix))]
        block_len = len(block[0])
        nums = [
            int("".join(line[k] for line in block if line[k] != " "))
            for k in range(block_len)
        ]

        op = operator.add if ops[i] == "+" else operator.mul
        start = 0 if ops[i] == "+" else 1
        result += reduce(op, nums, start)
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
