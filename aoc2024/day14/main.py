import math
import os
import re
from functools import reduce

from tqdm import tqdm

from aoc_helper.utils import ExclusiveTimeIt, load_lines
from aoc_helper.image import save_bitmap

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> list[tuple[int, int, int, int]]:
    robots = []
    for line in lines:
        match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        assert match is not None
        robots.append(tuple(int(match.group(k)) for k in range(1, 5)))
    return robots


def score(robots: list[tuple[int, int, int, int]], n: int, m: int) -> int:
    quadrants = [0] * 4
    n2, m2 = n // 2, m // 2
    for px, py, _, _ in robots:
        if px == n2 or py == m2:
            continue
        quadrants[2 * (px > n2) + (py > m2)] += 1
    return reduce(lambda acc, x: acc * x, quadrants, 1)


@timeit
def task1(robots: list[tuple[int, int, int, int]], n: int, m: int, steps: int) -> int:
    new_robots = []
    for px, py, vx, vy in robots:
        new_robots.append(
            (
                (px + steps * vx) % n,
                (py + steps * vy) % m,
                vx,
                vy,
            )
        )
    return score(new_robots, n, m)


@timeit
def task2(robots: list[tuple[int, int, int, int]], n: int, m: int) -> int:
    os.makedirs("frames", exist_ok=True)
    os.makedirs("frames_short", exist_ok=True)
    scores = []
    digits = math.ceil(math.log10(n * m))
    grid_large = [[False] * (10 * n) for _ in range(10 * m)]
    for idx in tqdm(range(1, n * m)):
        new_robots = []
        idx_h, idx_w = (idx % 100) // 10, (idx % 100) % 10
        grid = [[False] * (n) for _ in range(m)]
        for px, py, vx, vy in robots:
            new_robots.append(((px + vx) % n, (py + vy) % m, vx, vy))
            grid[new_robots[-1][1]][new_robots[-1][0]] = True
            grid_large[idx_h * m + new_robots[-1][1]][
                idx_w * n + new_robots[-1][0]
            ] = True
        scores.append((score(new_robots, n, m), idx))
        robots = new_robots
        save_bitmap(grid, f"frames/{idx:0{digits}}.pbm")
        if idx % 100 == 99 or idx == n * m - 1:
            save_bitmap(grid_large, f"frames_short/{idx//100:0{digits-2}}.pbm")
            grid_large = [[False] * (10 * n) for _ in range(10 * m)]
    scores.sort()
    print("\n".join(map(str, scores[:20])))
    print("...")
    print("\n".join(map(str, scores[-20:])))
    return 0


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(inp, 101, 103, 100)
    total_p2 = task2(inp, 101, 103)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
