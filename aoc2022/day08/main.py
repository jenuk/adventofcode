from time import perf_counter_ns


# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minute(s)", "hour(s)", "day(s)"]
    idx = 0
    prev = 0
    while idx+1 < len(lengths) and time >= lengths[idx+1]:
        idx += 1
        time, prev = time//lengths[idx], time%lengths[idx]

    out = f"{time}{units[idx]}"
    if 0 < prev and time < 100:
        out += f" {prev}{units[idx-1]}"
    return out


def read_data(filename="input.txt"):
    with open(filename) as file:
        content = file.read().strip()

    return process_data(content)

# Ignore above


def process_data(content):
    data = [list(map(int, line)) for line in content.split()]
    return data


def check_data(data):
    m = len(data[0])
    for line in data:
        assert len(line) == m, "non rectangular data"


def task1(data):
    visible = [[False]*len(line) for line in data]
    for i, line in enumerate(data):
        highest = -1
        for j, x in enumerate(line):
            if x > highest:
                visible[i][j] = True
                highest = x

        highest = -1
        for j, x in enumerate(line[::-1]):
            if x > highest:
                visible[i][-j-1] = True
                highest = x

    for j in range(len(data[0])):
        highest = -1
        for i in range(len(data)):
            if data[i][j] > highest:
                visible[i][j] = True
                highest = data[i][j]

        highest = -1
        for i in range(len(data)-1, -1, -1):
            if data[i][j] > highest:
                visible[i][j] = True
                highest = data[i][j]

    return sum(v for line in visible for v in line)


def get_scenic_score(data, i0, j0):
    height = data[i0][j0]
    scores = [0, 0, 0, 0]
    i = i0-1
    while i >= 0 and data[i][j0] < height:
        scores[0] += 1
        i -= 1
    if i != -1:
        scores[0] += 1
    i = i0+1
    while i < len(data) and data[i][j0] < height:
        scores[1] += 1
        i += 1
    if i != len(data):
        scores[1] += 1
    j = j0-1
    while j >= 0 and data[i0][j] < height:
        scores[2] += 1
        j -= 1
    if j != -1:
        scores[2] += 1
    j = j0+1
    while j < len(data[0]) and data[i0][j] < height:
        scores[3] += 1
        j += 1
    if j != len(data[i0]):
        scores[3] += 1
    return scores[0] * scores[1] * scores[2] * scores[3]



def task2(data):
    score = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data[i])-1):
            score = max(score, get_scenic_score(data, i, j))
    return score


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
    check_data(data)
    t1 = perf_counter_ns()
    result1 = task1(data)
    t2 = perf_counter_ns()
    result2 = task2(data)
    t3 = perf_counter_ns()

    print(f"Data preprocessing in {format_ns(t1 - t0)}")
    print(f"Task 1: {result1} in {format_ns(t2 - t1)}")
    print(f"Task 2: {result2} in {format_ns(t3 - t2)}")


if __name__ == "__main__":
    main()
