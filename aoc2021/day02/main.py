import numpy as np
import pandas as pd

def task1(data):
    return np.product(np.sum(data, axis=0))

def task2(data):
    aim = np.cumsum(data[:, 1])
    return np.sum(data[:, 0]) * np.sum(data[:, 0] * aim)

if __name__ == '__main__':
    df = pd.read_csv("input.txt", header=None, sep=" ")

    def inner(d):
        return [d[1]*(d[0]=="forward"), d[1]*((d[0]=="down") - (d[0]=="up"))]
    data = df.apply(inner, axis=1, result_type="expand").to_numpy()

    res1 = task1(data)
    res2 = task2(data)

    print(f"Task1: {res1}")
    print(f"Task2: {res2}")
