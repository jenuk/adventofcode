from dataclasses import dataclass
from itertools import product
from time import perf_counter_ns
from typing import DefaultDict, Dict, List, Set, Tuple

from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d


# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 0
    prev = 0
    while time > lengths[idx+1]:
        idx += 1
        time, prev = time//lengths[idx], time%lengths[idx]

    out = f"{time}{units[idx]}"
    if 0 < prev and time < 100:
        out += f" {prev}{units[idx-1]}"
    return out


def read_data(filename="input.txt"):
    with open(filename) as file:
        content = file.read().strip()

    return process_data(content)

# Ignore above


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    def adjacents(self):
        return [
            Point(self.x+1, self.y,   self.z),
            Point(self.x-1, self.y,   self.z),
            Point(self.x,   self.y+1, self.z),
            Point(self.x,   self.y-1, self.z),
            Point(self.x,   self.y,   self.z+1),
            Point(self.x,   self.y,   self.z-1),
        ]


def process_data(content: str) -> List[Point]:
    lines = content.split("\n")
    coordinates = [Point(*map(int, l.split(","))) for l in lines]
    # coordinates.sort(key=lambda p: p.x)
    return coordinates


def check_data(data):
    pass


def task1(data: List[Point]) -> int:
    data_dict = DefaultDict(lambda: DefaultDict(lambda: DefaultDict(bool)))
    for p in data:
        data_dict[p.x][p.y][p.z] = True
    # using sets seems to be slightly slower
    # data_set = set(data)
    result = 0
    for pt in data:
        for pt2 in pt.adjacents():
            result += not data_dict[pt2.x][pt2.y][pt2.z]
            # result += pt2 not in data_set
    return result


def task2(data):
    data_dict = DefaultDict(lambda: DefaultDict(lambda: DefaultDict(bool)))
    for p in data:
        data_dict[p.x][p.y][p.z] = True
    min_x = min(p.x for p in data)-1
    min_y = min(p.y for p in data)-1
    min_z = min(p.z for p in data)-1
    max_x = max(p.x for p in data)+1
    max_y = max(p.y for p in data)+1
    max_z = max(p.z for p in data)+1
    is_air = DefaultDict(lambda: DefaultDict(lambda: DefaultDict(bool)))
    stack = [
        [Point(min_x, y, z) for y, z in product(range(min_y, max_y),
                                                range(min_z, max_z))],
        [Point(max_x, y, z) for y, z in product(range(min_y, max_y),
                                                range(min_z, max_z))],
        [Point(x, min_y, z) for x, z in product(range(min_x, max_x),
                                                range(min_z, max_z))],
        [Point(x, max_y, z) for x, z in product(range(min_x, max_x),
                                                range(min_z, max_z))],
        [Point(x, y, min_z) for x, y in product(range(min_x, max_x),
                                                range(min_y, max_y))],
        [Point(x, y, max_z) for x, y in product(range(min_x, max_x),
                                                range(min_y, max_y))],
    ]
    stack = [p for line in stack for p in line]
    while len(stack) > 0:
        pt = stack.pop()
        if is_air[pt.x][pt.y][pt.z]:
            continue
        is_air[pt.x][pt.y][pt.z] = True
        for pt2 in pt.adjacents():
            if not (data_dict[pt2.x][pt2.y][pt2.z]
                    or is_air[pt2.x][pt2.y][pt2.z]
                    or pt2.x < min_x or pt2.x > max_x
                    or pt2.y < min_y or pt2.y > max_y
                    or pt2.z < min_z or pt2.z > max_z
                    ):
                stack.append(pt2)

    result = 0
    for pt in data:
        for pt2 in pt.adjacents():
            result += is_air[pt2.x][pt2.y][pt2.z]
    return result


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
    check_data(data)
    t1 = perf_counter_ns()
    result1 = task1(data)
    t2 = perf_counter_ns()
    result2 = task2(data)
    t3 = perf_counter_ns()

    print(f"Data preprocessing in {format_ns(t1 - t0)}")
    print(f"Task 1: {result1} in {format_ns(t2 - t1)}")
    print(f"Task 2: {result2} in {format_ns(t3 - t2)}")


if __name__ == "__main__":
    main()
