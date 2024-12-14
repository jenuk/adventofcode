from aoc_helper.utils import ExclusiveTimeIt, load_lines

timeit = ExclusiveTimeIt()

Game = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


@timeit
def prepare_input(lines: list[str]) -> list[Game]:
    line_it = iter(lines)
    games = []
    while True:
        try:
            game = []
            for k in range(3):
                line = next(line_it).replace("=", "+").split()
                x = int(line[-2].split("+")[-1].rstrip(","))
                y = int(line[-1].split("+")[-1])
                game.append((x, y))
            games.append(tuple(game))
            next(line_it)
        except StopIteration:
            break
    return games


@timeit
def task(games: list[Game], task2: bool) -> int:
    result = 0
    for (x_a, y_a), (x_b, y_b), (x_t, y_t) in games:
        if task2:
            x_t += 10000000000000
            y_t += 10000000000000

        # A @ k = t
        # A = {{x_a, x_b}, {y_a, y_b}}, t = {x_t, y_t}, k = {k_a, k_b}
        # A^-1 = 1/(x_a * y_b - x_b*y_a) * {{y_b, -x_b}, {-y_a, x_a}}
        # k = A^-1 @ t = 1/(...) * A' @ t =: 1/(d) * u
        d = x_a * y_b - x_b * y_a
        u_x = x_t * y_b - x_b * y_t
        u_y = -x_t * y_a + x_a * y_t
        if u_x % d != 0 or u_y % d != 0:
            continue
        k_a = u_x // d
        k_b = u_y // d
        result += 3 * k_a + k_b
    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task(inp, False)
    total_p2 = task(inp, True)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
