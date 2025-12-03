import math

from aoc_helper.utils import load_lines, ExclusiveTimeIt

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> list[list[int]]:
    return [list(map(int, line)) for line in lines]


@timeit
def task1(banks: list[list[int]]) -> int:
    result = 0
    for bank in banks:
        digit1 = max(bank[:-1])
        pos1 = bank.index(digit1)
        digit2 = max(bank[pos1 + 1 :])
        result += digit1 * 10 + digit2
    return result


@timeit
def task2(banks: list[list[int]], num_batteries: int = 12) -> int:
    result = 0
    for bank in banks:
        joltage = 0
        pos = -1
        for k in range(num_batteries):
            digit = max(bank[pos + 1 : len(bank) - (num_batteries - k - 1)])
            pos = bank.index(digit, pos + 1)
            joltage = 10 * joltage + digit
        result += joltage
    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(inp)
    total_p2 = task2(inp)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
