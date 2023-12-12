import math
from itertools import cycle
from aoc_helper.utils import load_lines, timeit


def find_cycle_length(
    start: str, dirs: list[str], graph: dict[str, tuple[str, str]]
) -> tuple[int, int]:
    dirs_cycle = cycle(dirs)
    arrived = {key: ([], []) for key in graph}
    steps = 0
    current = start
    z_location = None
    while steps % len(dirs) not in arrived[current][0]:
        arrived[current][0].append(steps % len(dirs))
        arrived[current][1].append(steps)
        current = graph[current][next(dirs_cycle) == "R"]
        steps += 1
        if current.endswith("Z"):
            z_location = steps
    arrived_idx = arrived[current][0].index(steps % len(dirs))
    assert z_location is not None, "No way to the target found"
    return z_location, steps - arrived[current][1][arrived_idx]


@timeit
def main(fn: str):
    lines = load_lines(fn)
    dirs = lines[0]
    lines = lines[2:]

    graph = dict()
    for line in lines:
        key, lr = line.split(" = ")
        left, right = lr[1:-1].split(", ")
        graph[key] = (left, right)

    total_p1 = 0
    total_p2 = 0

    current = "AAA"
    dirs_cycle = cycle(dirs)
    while current != "ZZZ":
        d = next(dirs_cycle)
        current = graph[current][int(d == "R")]
        total_p1 += 1

    # Following the instructions without stopping from any start point will
    # result in in a cycle by necessity.
    # Experimentally: The cycles in my example always have exactly one valid
    # end point in them. I will assume that this is a given, but it is not
    # actually stated in the text.
    # More experimentation: the cycle's end is always the target, will assume
    # this as well instead of bothering with the chinese remainer theorem

    current = [n for n in graph if n.endswith("A")]
    cycle_lens = [find_cycle_length(n, dirs, graph)[0] for n in current]
    total_p2 = 1
    # calculate lcd
    for k in cycle_lens:
        gcd = math.gcd(total_p2, k)
        total_p2 = (total_p2 * k) // gcd

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
