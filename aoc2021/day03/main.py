import numpy as np

def read_data(filename):
    with open(filename) as file:
        data = list(map(lambda x: list(map(int, x)), file.read().split()))

    return np.array(data)


def task1(data):
    gamma = (np.sum(data, axis=0) >= data.shape[0]/2) @ (2**np.arange(data.shape[1]-1, -1, -1))
    epsilon = ((1 << data.shape[1]) - 1) ^ gamma
    return gamma*epsilon


def task2(data):
    data_o = data
    data_c = data

    for b in range(data.shape[1]):
        if data_o.shape[0] > 1:
            common = np.sum(data_o[:, b], axis=0) >= data_o.shape[0]/2
            data_o = data_o[data_o[:, b] == common]


        if data_c.shape[0] > 1:
            common = np.sum(data_c[:, b], axis=0) >= data_c.shape[0]/2
            data_c = data_c[data_c[:, b] != common]

    vals = (2**np.arange(data.shape[1]-1, -1, -1))
    oxygen = data_o[0] @ vals
    co2    = data_c[0] @ vals

    return oxygen * co2


if __name__ == '__main__':
    data = read_data("input.txt")

    res1 = task1(data)
    res2 = task2(data)

    print(f"Task1: {res1}")
    print(f"Task2: {res2}")
