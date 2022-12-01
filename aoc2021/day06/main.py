import numpy as np


def read_data(filename):
    with open(filename) as file:
        data = list(map(int, file.read().strip().split(",")))

    array = np.zeros(9, dtype=np.int64)
    for k in data:
        array[k] += 1

    return array


def steps(data, n):
    mat = np.zeros((9, 9), dtype=np.int64)
    for i in range(1, 9):
        mat[i-1][i] = 1
    mat[6][0] = 1
    mat[8][0] = 1

    mat = np.linalg.matrix_power(mat, n)
    data = mat @ data

    return np.sum(data)


if __name__ == '__main__':
    data = read_data("input.txt")

    print("Task1:", steps(data, 80))
    print("Task2:", steps(data, 256))
