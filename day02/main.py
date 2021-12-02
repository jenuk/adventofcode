import numpy as np
import pandas as pd

def task1(direction, amount):
    return np.product(amount @ direction)

def task2(direction, amount):
    aim = np.cumsum(amount * direction[:, 1])
    horizontal = amount @ direction[:, 0]
    depth = (aim * amount) @ direction[:, 0]

    return horizontal*depth


if __name__ == '__main__':
    df = pd.read_csv("input.txt", header=None, sep=" ")

    direction = df[0].to_list()
    def dir_to_vec(d):
        return [d == "forward", (d == "down") - (d == "up")]
    direction = np.array(list(map(dir_to_vec, direction)))
    amount = df[1].to_numpy()

    res1 = task1(direction, amount)
    res2 = task2(direction, amount)

    print(f"Task1: {res1}")
    print(f"Task2: {res2}")
