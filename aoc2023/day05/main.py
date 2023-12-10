from aoc_helper.utils import load_lines, timeit


class Almanach:
    def __init__(self, lines: list[str]):
        instructions = [
            ((tp := tuple(map(int, line.split())))[1], tp[0], tp[2]) for line in lines
        ]
        instructions.sort()
        self.source = [line[0] for line in instructions]
        self.destination = [line[1] for line in instructions]
        self.ranges = [line[2] for line in instructions]

    def single(self, val: int) -> int:
        idx = -1
        while idx + 1 < len(self.source) and self.source[idx + 1] <= val:
            # TODO: this could be binary search
            idx += 1

        if idx == -1 or val >= self.source[idx] + self.ranges[idx]:
            # unmapped
            return val
        else:
            return self.destination[idx] + (val - self.source[idx])

    def interval(self, val: tuple[int, int], idx=-1) -> list[tuple[int, int]]:
        while idx + 1 < len(self.source) and self.source[idx + 1] <= val[0]:
            # TODO: this could be binary search
            idx += 1

        if idx == -1 or val[0] >= self.source[idx] + self.ranges[idx]:
            # unmapped
            affine = lambda x: x
            endpoint = self.source[idx + 1]
            idx += 1
        else:
            affine = lambda x: self.destination[idx] + (x - self.source[idx])
            endpoint = self.source[idx] + self.ranges[idx]

        out = [(affine(val[0]), affine(min(val[1], endpoint)))]
        if val[1] > endpoint:
            out += self.interval((endpoint, val[1]), idx=idx)
        return out


@timeit
def main(fn: str):
    lines = load_lines(fn)

    total_p1 = 0
    total_p2 = 0
    seeds = list(map(int, lines[0].split(":")[-1].split()))
    seeds_extented = [(v1, v1 + v2) for v1, v2 in zip(seeds[::2], seeds[1::2])]
    # assumes that almanachs are given in order
    almanachs = [
        Almanach(block.split("\n")[1:]) for block in "\n".join(lines[2:]).split("\n\n")
    ]

    for almanach in almanachs:
        seeds = [almanach.single(s) for s in seeds]
        seeds_extented = [
            curr for prev in seeds_extented for curr in almanach.interval(prev)
        ]
        # one could try to merge intervals here again
    total_p1 = min(seeds)
    total_p2 = min(min(seeds_extented))

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
