from collections import defaultdict

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[dict[str, list[tuple[int, int]]], int, int]:
    antennas: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch != ".":
                antennas[ch].append((i, j))
    return antennas, len(lines), max(map(len, lines))


def is_inside(x: int, y: int, n: int, m: int) -> bool:
    return (0 <= x < n) and (0 <= y < m)


@timeit
def task1(antennas: dict[str, list[tuple[int, int]]], n: int, m: int) -> int:
    signals = set()
    for ch, locations in antennas.items():
        for k, loc_a in enumerate(locations):
            for loc_b in locations[k + 1 :]:
                delta = (loc_a[0] - loc_b[0], loc_a[1] - loc_b[1])
                x, y = loc_a[0] + delta[0], loc_a[1] + delta[1]
                if is_inside(x, y, n, m):
                    signals.add((x, y))
                x, y = loc_b[0] - delta[0], loc_b[1] - delta[1]
                if is_inside(x, y, n, m):
                    signals.add((x, y))
    return len(signals)


@timeit
def task2(antennas: dict[str, list[tuple[int, int]]], n: int, m: int) -> int:
    signals = set()
    max_signals = max(n, m)
    for ch, locations in antennas.items():
        for k, loc_a in enumerate(locations):
            for loc_b in locations[k + 1 :]:
                delta = (loc_a[0] - loc_b[0], loc_a[1] - loc_b[1])
                for nu in range(max_signals + 1):
                    found = False
                    for d in [-1, 1]:
                        x, y = (
                            loc_a[0] + d * nu * delta[0],
                            loc_a[1] + d * nu * delta[1],
                        )
                        if is_inside(x, y, n, m):
                            signals.add((x, y))
                            found = True
                    if not found:
                        break
    return len(signals)


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
