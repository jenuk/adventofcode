import itertools
from typing import Iterator

from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.grid import Grid
from aoc_helper.graph import BaseNode, dijkstra

timeit = ExclusiveTimeIt()

keypad_num_grid = Grid(
    4,
    3,
    [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [".", "0", "A"],
    ],
)
keypad_num_v2l = {val: (i, j) for i, j, val in keypad_num_grid if val != "."}

keypad_dir_grid = Grid(
    2,
    3,
    [
        [".", "^", "A"],
        ["<", "v", ">"],
    ],
)
keypad_dir_v2l = {val: (i, j) for i, j, val in keypad_dir_grid if val != "."}

keypads = {
    "num": {"grid": keypad_num_grid, "v2l": keypad_num_v2l},
    "dir": {"grid": keypad_dir_grid, "v2l": keypad_dir_v2l},
}
translate = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1), "A": "A"}


class CostBasedNode(BaseNode):
    has_unique = True

    def __init__(
        self,
        last_button: str,
        location: str,
        preseed: str | None,
        movement_cost: dict[tuple[str, str], int],
        keypad_type: str,
    ):
        self.last_button = last_button
        self.location = location
        self.pressed = preseed
        self.movement_cost = movement_cost
        self.keypad_type = keypad_type

    def unique(self) -> tuple[str, str, str | None]:
        return (self.last_button, self.location, self.pressed)

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["CostBasedNode", int]]:
        assert not reverse
        if self.pressed is not None:
            return

        for button in translate.keys():
            cost = self.movement_cost[(self.last_button, button)]
            if button == "A":
                yield (
                    CostBasedNode(
                        "A",
                        self.location,
                        self.location,
                        self.movement_cost,
                        self.keypad_type,
                    ),
                    cost,
                )
            else:
                di, dj = translate[button]
                i, j = keypads[self.keypad_type]["v2l"][self.location]
                i, j = i + di, j + dj
                if (val := keypads[self.keypad_type]["grid"].get(i, j, ".")) != ".":
                    yield (
                        CostBasedNode(
                            button, val, None, self.movement_cost, self.keypad_type,
                        ),
                        cost,
                    )


def get_cost_tower(n: int):
    if n <= 0:
        raise ValueError(f"Invalid {n}")

    current_cost = {
        combination: 1
        for combination in itertools.product(keypad_dir_v2l, keypad_dir_v2l)
    }
    all_keypad_types = ["dir"] * n
    all_keypad_types.append("num")
    for keypad_type in all_keypad_types:
        next_cost = dict()
        for start_val in keypads[keypad_type]["v2l"]:
            for node, _, cost in dijkstra(
                CostBasedNode("A", start_val, None, current_cost, keypad_type)
            ):
                if node.pressed is not None:
                    next_cost[(start_val, node.pressed)] = cost
        current_cost = next_cost
    return current_cost


@timeit
def task1(lines: list[str], tower: int = 2) -> int:
    all_distances = get_cost_tower(tower)
    result = 0
    for line in lines:
        base_val = int("".join(ch for ch in line if ch != "A"))
        length = 0
        line = "A" + line
        for ch1, ch2 in zip(line[:-1], line[1:]):
            length += all_distances[(ch1, ch2)]
        result += base_val * length
    return result


@timeit
def task2(lines: list[str]) -> int:
    return task1(lines, tower=25)


def main(fn: str):
    lines = load_lines(fn)

    total_p1 = task1(lines)
    total_p2 = task2(lines)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
