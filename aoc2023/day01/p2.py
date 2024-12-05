import re


def main(fn):
    with open(fn) as f:
        lines = f.read().strip().split("\n")

    translate = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }

    total = 0
    for line in lines:
        ch1 = None
        ch2 = None
        line = line + " "
        for k in range(len(line) - 1):
            for key, val in translate.items():
                if ch1 is None and line[k:].startswith(key):
                    ch1 = val
                if ch2 is None and line[: -k - 1].endswith(key):
                    ch2 = val
            if ch1 is not None and ch2 is not None:
                break
        assert ch1 is not None and ch2 is not None
        total += 10 * ch1 + ch2
    print(total)


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
