from collections import defaultdict

from aoc_helper.utils import load_lines, ExclusiveTimeIt


timeit = ExclusiveTimeIt()


@timeit
def prepare_input(lines: list[str]) -> tuple[list[int]]:
    return (list(map(int, lines)),)


def mix_prune(x: int, y: int) -> int:
    # 16_777_216 = 2**24
    return (x ^ y) % 16_777_216


def next_secret(x: int) -> int:
    x = mix_prune(x, 64 * x)
    x = mix_prune(x, x // 32)
    return mix_prune(x, 2048 * x)


@timeit
def task1(secret_numbers: list[int]) -> int:
    result = 0
    for x in secret_numbers:
        for _ in range(2_000):
            x = next_secret(x)
        result += x
    return result


@timeit
def task2(secret_numbers: list[int]) -> int:
    sequence_to_price = defaultdict(int)
    for x in secret_numbers:
        current_sequences = set()
        cycle_store = tuple()
        y_prev = x % 10
        for _ in range(2_000):
            x = next_secret(x)
            y = x % 10
            cycle_store = cycle_store + (y - y_prev,)
            if len(cycle_store) < 4:
                continue
            elif len(cycle_store) > 4:
                cycle_store = cycle_store[1:]
            new = cycle_store
            if new in current_sequences:
                continue
            current_sequences.add(new)
            sequence_to_price[new] += y

    return max(sequence_to_price.values())


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
