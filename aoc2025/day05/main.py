import math

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


def bisect_biggest(a, b, check) -> int:
    assert check(a)
    while a < b:
        m = math.ceil((a + b) / 2)
        if check(m):
            a = m
        else:
            b = m - 1
    return a


class Interval:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def __contains__(self, num) -> bool:
        if not isinstance(num, int):
            return False

        return self.a <= num <= self.b

    def merge(self, other: "Interval") -> "Interval | None":
        if other.a in self or self.a in other:
            return Interval(min(self.a, other.a), max(self.b, other.b))
        else:
            return None


class UnionOfIntervals:
    def __init__(self, intervals: list[Interval] | None = None):
        self.intervals: list[Interval] = []

        if intervals:
            intervals.sort(key=lambda interval: interval.a)
            self.intervals.append(intervals[0])
            for interval in intervals[1:]:
                if (merge := interval.merge(self.intervals[-1])) is not None:
                    self.intervals[-1] = merge
                else:
                    self.intervals.append(interval)

    def add_interval(self, interval: Interval):
        if len(self.intervals) == 0:
            self.intervals.append(interval)
            return

        if interval.a < self.intervals[0].a:
            if (merge := interval.merge(self.intervals[0])) is not None:
                self.intervals[0] = merge
            else:
                self.intervals.insert(0, interval)
            return

        index = bisect_biggest(
            0,
            len(self.intervals) - 1,
            lambda idx: self.intervals[idx].a <= interval.a,
        )
        if (merge := interval.merge(self.intervals[index])) is not None:
            self.intervals[index] = merge
            while (index + 1 < len(self.intervals)) and (
                merge := self.intervals[index].merge(self.intervals[index + 1])
            ) is not None:
                self.intervals[index] = merge
                self.intervals.pop(index + 1)
        elif index + 1 < len(self.intervals) and (
            merge := interval.merge(self.intervals[index + 1])
        ):
            index += 1
            self.intervals[index] = merge
            while (index + 1 < len(self.intervals)) and (
                merge := self.intervals[index].merge(self.intervals[index + 1])
            ) is not None:
                self.intervals[index] = merge
                self.intervals.pop(index + 1)
        else:
            self.intervals.insert(index + 1, interval)

    def __contains__(self, num) -> bool:
        if not isinstance(num, int):
            return False

        if len(self.intervals) == 0 or num < self.intervals[0].a:
            return False

        index = bisect_biggest(
            0, len(self.intervals) - 1, lambda idx: self.intervals[idx].a <= num
        )
        return num in self.intervals[index]


@timeit
def prepare_input(lines: list[str]) -> tuple[UnionOfIntervals, list[int]]:
    split_idx = lines.index("")
    intervals_str = lines[:split_idx]
    intervals = []
    for interval_str in intervals_str:
        a, b = interval_str.split("-")
        intervals.append(Interval(int(a), int(b)))
    uoi = UnionOfIntervals(intervals)
    inventory = list(map(int, lines[split_idx + 1 :]))
    return uoi, inventory


@timeit
def task1(uoi: UnionOfIntervals, inventory: list[int]) -> int:
    result = 0
    for item in inventory:
        result += item in uoi
    return result


@timeit
def task2(uoi: UnionOfIntervals, inventory: list[int]) -> int:
    result = 0
    for interval in uoi.intervals:
        # both ends are inclusive, add 1
        result += interval.b - interval.a + 1
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
