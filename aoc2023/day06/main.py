import math

from aoc_helper.utils import load_lines, timeit


def get_num_solutions(time: int, best: int) -> int:
    # distance travelled is x * (t - x) where t total time, x time pressed
    # = -x^2 + t*x
    # optimium is x = t/2

    # x * (t - x) > v
    # <=> x^2 - tx + v > 0
    # x^2 - tx + v = 0
    # x = t/2 +/- sqrt((t/2)^2 - v)
    # upper range limit: floor(t/2 + sqrt(...))
    # lower range limit: ceil(t/2 - sqrt(...))
    root = math.sqrt((time / 2) ** 2 - best)
    lower = math.ceil(time / 2 - root)
    upper = math.floor(time / 2 + root)
    # both ranges are inclusive -> add 1
    return upper - lower + 1


@timeit
def main(fn: str):
    lines = load_lines(fn)
    times = list(map(int, lines[0].split(":")[-1].strip().split()))
    distances = list(map(int, lines[1].split(":")[-1].strip().split()))

    total_p1 = 1
    for t, v in zip(times, distances):
        total_p1 *= get_num_solutions(t, v)

    time = int("".join([x for x in lines[0] if x.isnumeric()]))
    distance = int("".join([x for x in lines[1] if x.isnumeric()]))
    total_p2 = get_num_solutions(time, distance)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
