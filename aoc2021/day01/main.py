import numpy as np

def task1(data):
    return np.sum(data[1:] > data[:-1])

def task2(data):
    return np.sum(data[3:] > data[:-3])

if __name__ == '__main__':
    with open("input.txt") as file:
        data = np.array(list(map(int, file.readlines())))

    res1 = task1(data)
    res2 = task2(data)

    print(f"Task1 {res1}")
    print(f"Task2 {res2}")

