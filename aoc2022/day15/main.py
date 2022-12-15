from __future__ import annotations

import re
from time import perf_counter_ns
from typing import Optional

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


def process_data(content):
    pattern = re.compile(
        r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): "
        r"closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
    )
    sensors = []
    for line in content.split("\n"):
        match = re.match(pattern, line)
        assert match is not None, repr(line)
        sensor = (int(match.group("sensor_x")), int(match.group("sensor_y")))
        beacon = (int(match.group("beacon_x")), int(match.group("beacon_y")))
        sensors.append((sensor, beacon))
    return sensors


def check_data(data):
    pass

class Interval:
    def __init__(self, a: int, b: int) -> None:
        assert a <= b, "no interval"
        self.a = a
        self.b = b

    def overlap(self, other: Interval) -> bool:
        # returns true, even if they are just adjacent
        if self.a <= other.a:
            return self.b+1 >= other.a
        else:
            return other.b+1 >= self.a

    def union(self, other: Interval) -> Interval:
        if not self.overlap(other):
            raise ValueError("No overlap")
        return Interval(min(self.a, other.a), max(self.b, other.b))

    def contains(self, x: int) -> bool:
        return self.a <= x <= self.b

    def length(self) -> int:
        return self.b - self.a + 1 

    def __str__(self) -> str:
        return f"[{self.a}, {self.b}]"

class Menge:
    def __init__(self, *intervals: Interval):
        self.intervals = list(intervals)

    def add(self, other: Interval):
        if len(self.intervals) == 0:
            self.intervals = [other]
            return
        i = -1
        for k, inter in enumerate(self.intervals):
            if inter.a <= other.a:
                i = k
            else:
                break

        if 0 <= i and other.overlap(self.intervals[i]):
            other = other.union(self.intervals[i])
            k = i+1
            while (k < len(self.intervals)
                    and other.overlap(self.intervals[k])):
                other = other.union(self.intervals[k])
                k += 1
            self.intervals[i:k] = [other]
        elif i+1 < len(self.intervals) and other.overlap(self.intervals[i+1]):
            other = other.union(self.intervals[i+1])
            k = i+2
            while (k < len(self.intervals)
                    and other.overlap(self.intervals[k])):
                other = other.union(self.intervals[k])
                k += 1
            self.intervals[i+1:k] = [other]
        else:
            self.intervals.insert(i+1, other)

    def contains(self, x: int) -> bool:
        for interval in self.intervals:
            if interval.contains(x):
                return True
        return False
    
    def length(self) -> int:
        return sum(i.length() for i in self.intervals)

    def __str__(self) -> str:
        return ", ".join(map(str, self.intervals))


def task1(data, ylevel=2_000_000):
    data = sorted(data, key=lambda x: x[0][0])
    occupied = Menge()
    beacons: set[int] = set()
    for (sx, sy), (bx, by) in data:
        if by == ylevel:
            beacons.add(bx)
        dist = abs(sx - bx) + abs(sy - by)
        dy = abs(ylevel - sy)
        if dy > dist:
            continue
        startx = sx - (dist - dy)
        endx   = sx + (dist - dy)
        occupied.add(Interval(startx, endx))
    return occupied.length() - sum(occupied.contains(x) for x in beacons)


def task2(data):
    bound = Interval(0, 4_000_000)
    data = sorted(data, key=lambda x: x[0][0])
    for ylevel in range(bound.b, bound.a-1, -1):
        occupied = Menge()
        for (sx, sy), (bx, by) in data:
            dist = abs(sx - bx) + abs(sy - by)
            dy = abs(ylevel - sy)
            if dy > dist:
                continue
            startx = max(sx - (dist - dy), bound.a)
            endx   = min(sx + (dist - dy), bound.b)
            occupied.add(Interval(startx, endx))
        if occupied.length() < bound.length():
            if not occupied.contains(0):
                xloc = bound.a
            elif not occupied.contains(bound.b):
                xloc = bound.b
            else:
                assert len(occupied.intervals) == 2, str(occupied)
                xloc = occupied.intervals[0].b+1
            yloc = ylevel
            return 4000000*xloc + yloc
    raise ValueError("Did not find any unoccupied spaces")


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
