def get_neighbors(i: int, j: int, n: int, m: int):
    for k in range(-1, 2):
        for l in range(-1, 2):
            if k == 0 and l == 0:
                continue
            if 0 <= i + k < n and 0 <= j + l < m:
                yield (i + k, j + l)


def main(fn: str):
    with open(fn, "r") as f:
        lines = f.read().strip().split("\n")

    n, m = len(lines), len(lines[0])
    is_p1 = [[False] * len(l) for l in lines]
    gear_neighbors = [[[] for _ in range(m)] for _ in range(n)]
    gear_nums = dict()

    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch == "." or ch.isnumeric():
                continue

            for k, l in get_neighbors(i, j, n, m):
                is_p1[k][l] = True
                if ch == "*":
                    gear_neighbors[k][l].append((i, j))
                    gear_nums[(i, j)] = []

    total_p1 = 0
    total_p2 = 0
    for line, to_add_line, gears_line in zip(lines, is_p1, gear_neighbors):
        tally_num = 0
        tally_add = False
        tally_gears = []
        for ch, to_add, gears in zip(line, to_add_line, gears_line):
            if not ch.isnumeric():
                if tally_num != "" and tally_add:
                    total_p1 += tally_num
                    for gear in set(tally_gears):
                        gear_nums[gear].append(tally_num)
                tally_num = 0
                tally_add = False
                tally_gears = []
            else:
                tally_num = 10 * tally_num + int(ch)
                tally_add = tally_add or to_add
                tally_gears.extend(gears)
        if tally_num != "" and tally_add:
            total_p1 += tally_num
            for gear in set(tally_gears):
                gear_nums[gear].append(tally_num)

    for gear_parts in gear_nums.values():
        if len(gear_parts) == 2:
            total_p2 += gear_parts[0] * gear_parts[1]

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
