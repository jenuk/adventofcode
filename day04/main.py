import numpy as np

def read_data(filename):
    with open(filename) as file:
        data = file.read()

    data = data.split("\n\n")
    nums = list(map(int, data[0].split(",")))
    data = data[1:]
    data = [[x.replace("  ", " ").strip().split(" ") for x in bingo.strip().split("\n")] for bingo in data]
    data = np.array(data, dtype=int)

    return nums, data

def task1(nums, data):
    marked = np.zeros_like(data)
    for num in nums:
        marked[data == num] = 1

        inds = np.max(np.sum(marked, axis=1), axis=1) == marked.shape[2]
        if np.sum(inds) > 0:
            return np.sum(data[inds][np.logical_not(marked[inds])]) * num
            
        inds = np.max(np.sum(marked, axis=2), axis=1) == marked.shape[2]
        if np.sum(inds) > 0:
            return np.sum(data[inds][np.logical_not(marked[inds])]) * num

    raise ValueError("No winning board found")


def task2(nums, data):
    marked = np.zeros_like(data, dtype=bool)
    for num in nums:
        marked[data == num] = 1

        inds = np.max(np.sum(marked, axis=1), axis=1) != marked.shape[2]
        if np.sum(inds) < data.shape[0]:
            if data.shape[0] == 1:
                return np.sum(data[0][np.logical_not(marked[0])]) * num
            else:
                data = data[inds]
                marked = marked[inds]
            

        inds = np.max(np.sum(marked, axis=2), axis=1) != marked.shape[2]
        if np.sum(inds) < data.shape[0]:
            if data.shape[0] == 1:
                return np.sum(data[0][np.logical_not(marked[0])]) * num
            else:
                data = data[inds]
                marked = marked[inds]

    raise ValueError("Not all boards win")

if __name__ == '__main__':
    nums, data = read_data("input.txt")

    res1 = task1(nums, data)
    res2 = task2(nums, data)

    print(f"Task1: {res1}")
    print(f"Task2: {res2}")
