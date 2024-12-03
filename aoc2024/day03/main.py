import re

from aoc_helper.utils import load_lines, timeit


@timeit
def task1(lines: list[str]) -> int:
    result = 0
    for line in lines:
        for match in re.finditer(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", line):
            result += int(match.group(1)) * int(match.group(2))
    return result


@timeit
def task2(lines: list[str]) -> int:
    result = 0
    enabled = True
    for line in lines:
        mul_pattern = r"mul\(([0-9]{1,3}),([0-9]{1,3})\)"
        do_pattern = r"do\(\)"
        dont_pattern = r"don't\(\)"
        for match in re.finditer(rf"{mul_pattern}|{do_pattern}|{dont_pattern}", line):
            if match.group(0).startswith("don't"):
                enabled = False
            elif match.group(0).startswith("do"):
                enabled = True
            elif enabled:
                result += int(match.group(1)) * int(match.group(2))
    return result


@timeit
def main(fn: str):
    lines = load_lines(fn)

    total_p1 = task1(lines)
    total_p2 = task2(lines)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
