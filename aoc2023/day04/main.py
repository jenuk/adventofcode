from aoc_helper.utils import load_lines, timeit


@timeit
def main(fn: str):
    lines = load_lines(fn)

    total_p1 = 0
    total_p2 = [1] * len(lines)

    for k, line in enumerate(lines):
        _, line = line.split(":")
        winning, actual = line.split("|")
        winning = set(map(int, winning.split()))
        actual = list(map(int, actual.split()))
        matches = sum(a in winning for a in actual)
        if matches > 0:
            total_p1 += 2 ** (matches - 1)
            part = slice(k + 1, k + 1 + matches)
            total_p2[part] = [total_p2[k] + x for x in total_p2[part]]

    print(total_p1)
    print(sum(total_p2))


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
