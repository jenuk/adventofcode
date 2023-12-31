from enum import Enum
from typing import Any, Iterator, Optional

from aoc_helper.graph import BaseNode
from aoc_helper.graph_traversal import dijkstra
from aoc_helper.utils import timeit


class Amphipods(Enum):
    EMPTY = (-1, 0)
    A = (0, 1)
    B = (1, 10)
    C = (2, 100)
    D = (3, 1000)

    @property
    def tunnel(self):
        return self.value[0]

    @property
    def cost(self):
        return self.value[1]

    def __str__(self) -> str:
        return self.name if self != Amphipods.EMPTY else "."


class State(BaseNode):
    # tunnels: 4 x (2 | 4)
    # hallway [iixixixixii], x are always empty
    #          01234567890
    moveable_hallways = frozenset([0, 1, 3, 5, 7, 9, 10])
    tid_to_hallway = {0: 2, 1: 4, 2: 6, 3: 8}

    def __init__(
        self,
        tunnels: tuple[tuple[Amphipods, ...], ...],
        hallway: Optional[tuple[Amphipods, ...]] = None,
        heuristic: Optional[int] = None,
    ):
        self.tunnels = tunnels
        self.hallway = (
            hallway
            if hallway is not None
            else tuple(Amphipods.EMPTY for _ in range(11))
        )
        self.heuristic = heuristic

    def tunnel_ready(self, tid: int) -> bool:
        return all(a == Amphipods.EMPTY or a.tunnel == tid for a in self.tunnels[tid])

    def tunnel_finished(self, tid: int) -> bool:
        return all(a.tunnel == tid for a in self.tunnels[tid])

    def finished(self) -> bool:
        return all(self.tunnel_finished(tid) for tid in range(4))

    def expand(self) -> "State":
        new_tunnels = (
            (self.tunnels[0][0], Amphipods.D, Amphipods.D, self.tunnels[0][1]),
            (self.tunnels[1][0], Amphipods.C, Amphipods.B, self.tunnels[1][1]),
            (self.tunnels[2][0], Amphipods.B, Amphipods.A, self.tunnels[2][1]),
            (self.tunnels[3][0], Amphipods.A, Amphipods.C, self.tunnels[3][1]),
        )
        return State(new_tunnels)

    def check_movable(
        self,
        hallway_pos: int,
        tid: int,
        from_hallway: bool,
    ) -> bool:
        """Check if it is possible to move between tunnel tid and hallway_pos"""
        target_hallway = self.tid_to_hallway[tid]
        # if coming from the hallway, we need to skip checking that field, otherwise
        # we will need to check it.
        if hallway_pos < target_hallway:
            min_x, max_x = hallway_pos + from_hallway, target_hallway
        else:
            min_x, max_x = target_hallway, hallway_pos - from_hallway
        return all(self.hallway[k] == Amphipods.EMPTY for k in range(min_x, max_x + 1))

    def calc_dist(self, hallway_pos: int, tid: int, tunnel_pos: int) -> int:
        target_hallway = self.tid_to_hallway[tid]
        return abs(hallway_pos - target_hallway) + tunnel_pos + 1

    def try_move(
        self,
        hallway_pos: int,
        tid: int,
        from_hallway: bool,
        tunnel_pos: Optional[int] = None,
    ) -> tuple["State", int] | None:
        if not self.check_movable(hallway_pos, tid, from_hallway=from_hallway):
            return None
        if tunnel_pos is None:
            for k in range(len(self.tunnels[tid])):
                if self.tunnels[tid][k] == Amphipods.EMPTY:
                    tunnel_pos = k
                else:
                    break
            if tunnel_pos is None:
                return None

        # calculate cost
        dist = self.calc_dist(hallway_pos, tid, tunnel_pos)
        # one of them is 0
        cost = self.hallway[hallway_pos].cost + self.tunnels[tid][tunnel_pos].cost

        # generate new state
        new_tunnels = (
            *self.tunnels[:tid],
            (
                *self.tunnels[tid][:tunnel_pos],
                self.hallway[hallway_pos],
                *self.tunnels[tid][tunnel_pos + 1 :],
            ),
            *self.tunnels[tid + 1 :],
        )
        new_hallway = (
            *self.hallway[:hallway_pos],
            self.tunnels[tid][tunnel_pos],
            *self.hallway[hallway_pos + 1 :],
        )

        return State(new_tunnels, new_hallway), dist * cost

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["State", int]]:
        assert reverse is False, "Not implemented"

        # clear tunnel
        for tid, tunnel in enumerate(self.tunnels):
            if self.tunnel_ready(tid):
                # no need to clear the tunnel
                continue

            for k, amph in enumerate(tunnel):
                if amph == Amphipods.EMPTY:
                    continue

                for hallway_pos in self.moveable_hallways:
                    out = self.try_move(
                        hallway_pos, tid, tunnel_pos=k, from_hallway=False
                    )
                    if out is not None:
                        yield out
                break

        # fill tunnel
        for pos, amph in enumerate(self.hallway):
            if amph == Amphipods.EMPTY or not self.tunnel_ready(amph.tunnel):
                continue

            out = self.try_move(pos, amph.tunnel, from_hallway=True)
            if out is not None:
                yield out

        # guarantee a yield statement
        yield from ()

    def __hash__(self) -> int:
        return hash((self.tunnels, self.hallway))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, State):
            return False
        return self.hallway == other.hallway and self.tunnels == other.tunnels

    def __str__(self) -> str:
        line = "░░░{}░{}░{}░{}░░░\n"
        line_len = len(line.format(0, 0, 0, 0)) - 1

        result = "░" * line_len + "\n"
        result += "░" + "".join(map(str, self.hallway)) + "░\n"
        for k in range(len(self.tunnels[0])):
            result += line.format(*(self.tunnels[i][k] for i in range(4)))
        result += "░" * line_len
        return result


def read_data(filename="input.txt") -> str:
    with open(filename) as file:
        content = file.read().strip()
    return content


def process_data(content: str) -> State:
    lines = content.split("\n")
    tunnels = (
        (Amphipods[lines[2][3]], Amphipods[lines[3][3]]),
        (Amphipods[lines[2][5]], Amphipods[lines[3][5]]),
        (Amphipods[lines[2][7]], Amphipods[lines[3][7]]),
        (Amphipods[lines[2][9]], Amphipods[lines[3][9]]),
    )
    return State(tunnels)


@timeit
def main(fn: str):
    total_p1 = 0
    total_p2 = 0

    start = process_data(read_data(fn))
    start2 = start.expand()
    for node, _, distance in dijkstra(start, start_weight=0):
        if node.finished():
            total_p1 = distance
            break
    else:
        print("No solution found (p1)")

    for node, _, distance in dijkstra(start2, start_weight=0):
        if node.finished():
            total_p2 = distance
            break
    else:
        print("No solution found (p2)")

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
