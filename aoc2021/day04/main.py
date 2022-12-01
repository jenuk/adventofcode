import numpy as np

def read_data(filename):
    with open(filename) as file:
        data = file.read()

    data = data.split("\n\n")
    nums = list(map(int, data[0].split(",")))
    data = data[1:]
    data = [[x.split() for x in bingo.strip().split("\n")] for bingo in data]
    data = np.array(data, dtype=int)

    return nums, data


def get_scores(nums, data):
    marked = np.zeros_like(data, dtype=bool)
    scores = np.zeros(data.shape[0], dtype=int)
    start = 0

    for num in nums:
        marked[data == num] = True

        def check(d):
            inds = np.max(np.sum(marked, axis=d), axis=1) == marked.shape[d]
            if inds.any():
                pos = np.arange(marked.shape[0])[inds]
                end = start + pos.shape[0]
                scores[start:end] = np.sum(data[pos] * ~marked[pos], axis=(1,2)) * num
                return end, data[~inds], marked[~inds]
            else:
                return start, data, marked

        start, data, marked = check(1)
        start, data, marked = check(2)

    return scores


if __name__ == '__main__':
    nums, data = read_data("input.txt")
    
    scores = get_scores(nums, data)

    res1 = scores[0]
    res2 = scores[-1]

    print(f"Task1: {res1}")
    print(f"Task2: {res2}")
