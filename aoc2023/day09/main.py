from aoc_helper.utils import load_lines, timeit


def find_end(line: list[int]) -> int:
    last_elements = []
    while not all(x == 0 for x in line):
        last_elements.append(line[-1])
        line = [y - x for x, y in zip(line[:-1], line[1:])]
    z = 0
    for x in last_elements[::-1]:
        z = z + x
    return z


def find_start(line: list[int]) -> int:
    first_elements = []
    while not all(x == 0 for x in line):
        first_elements.append(line[0])
        line = [y - x for x, y in zip(line[:-1], line[1:])]
    z = 0
    for x in first_elements[::-1]:
        # x - z' = z -> z' = x - z
        z = x - z
    return z


@timeit
def main(fn: str):
    lines = load_lines(fn)

    total_p1 = 0
    total_p2 = 0

    for line in lines:
        li = list(map(int, line.split()))
        total_p1 += find_end(li)
        total_p2 += find_start(li)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
