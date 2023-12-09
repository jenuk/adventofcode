from collections import defaultdict


def main(fn: str):
    with open(fn, "r") as f:
        lines = f.read().strip().split("\n")

    max_cubes = dict()
    max_cubes["red"] = 12
    max_cubes["green"] = 13
    max_cubes["blue"] = 14

    total_p1 = 0
    total_p2 = 0
    for line in lines:
        info, game = line.split(":")
        game_number = int(info[5:])
        subgames = [
            [
                (int((h := hand.strip().split(" "))[0]), h[1])
                for hand in subgame.split(",")
            ]
            for subgame in game.split(";")
        ]

        works = True
        min_cubes = {"red": 0, "green": 0, "blue": 0}
        for subgame in subgames:
            for count, cube in subgame:
                min_cubes[cube] = max(min_cubes[cube], count)
                if max_cubes[cube] < count:
                    works = False

        total_p2 += min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
        if works:
            total_p1 += game_number

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
