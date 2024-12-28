from collections import defaultdict
import itertools

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[list[list[int]], list[list[int]], int]:
    full = "\n".join(lines)  # re-joining, don't want to touch my template
    blocks = [block.split("\n") for block in full.split("\n\n")]
    keys = []
    locks = []
    n = len(blocks[0])
    m = len(blocks[0][0])
    for block in blocks:
        # assumes every lock/key is actually continous
        # tasks describes all these numbers as -1
        obj = [sum(block[i][j] == "#" for i in range(n)) for j in range(m)]
        (keys if block[0][0] == "." else locks).append(obj)
    return keys, locks, n


@timeit
def task1(keys: list[list[int]], locks: list[list[int]], depth: int) -> int:
    result = 0
    for key, lock in itertools.product(keys, locks):
        result += all(k + l <= depth for k, l in zip(key, lock))
    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(*inp)

    print(f"Task 1: {total_p1}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
