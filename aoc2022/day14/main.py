from copy import deepcopy
from enum import Enum
from time import perf_counter_ns
from typing import List


# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 0
    prev = 0
    while time > lengths[idx+1]:
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

class Field(Enum):
    EMPTY = 0
    SOLID = 1
    SAND  = 2 # There is no real difference to SOLID
    SOURCE  = 3
    
    def __str__(self) -> str:
        if self == Field.EMPTY:
            return " "
        elif self == Field.SOLID:
            return "#"
        elif self == Field.SAND:
            return "o"
        elif self == Field.SOURCE:
            return "+"
        else:
            raise NotImplementedError("Unknown Type")


def process_data(content):
    data = [line.split("->") for line in content.split("\n")]
    # calculate min/max in each dimension, choose sand origin (500, 0)
    # as starting point
    xmin = 500
    xmax = 500
    ymin = 0
    ymax = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            a, b = data[i][j].split(",")
            a, b, = int(a), int(b)
            data[i][j] = (a, b)
            xmin = min(xmin, a)
            xmax = max(xmax, a)
            ymin = min(ymin, b)
            ymax = max(ymax, b)
    # spatial resolution is low -> can convert to dense matrix
    area = [[Field.EMPTY for _ in range(1+ymax-ymin)] for _ in range(1+xmax - xmin)]
    for line in data:
        for (x1, y1), (x2, y2) in zip(line[:-1], line[1:]):
            if x1 == x2:
                for t in range(min(y1, y2), max(y1, y2)+1):
                    area[x1-xmin][t-ymin] = Field.SOLID
            else:
                for t in range(min(x1, x2), max(x1, x2)+1):
                    area[t-xmin][y1-ymin] = Field.SOLID
    area[500 - xmin][0 - ymin] = Field.SOURCE
    return area, 500 - xmin, 0 - ymin


def check_data(data):
    pass

def out_of_bounds(x, y, n, m):
    return x < 0 or n <= x or y < 0 or m <= y

def simulate_and_place(area: List[List[Field]], x: int, y: int):
    n, m = len(area), len(area[0])
    while True:
        if out_of_bounds(x, y, n, m):
            # free-fall
            return False
        if out_of_bounds(x, y+1, n, m) or area[x][y+1] == Field.EMPTY:
            y = y+1
        elif out_of_bounds(x-1, y+1, n, m) or area[x-1][y+1] == Field.EMPTY:
            x, y = x-1, y+1
        elif out_of_bounds(x+1, y+1, n, m) or area[x+1][y+1] == Field.EMPTY:
            x, y = x+1, y+1
        else:
            area[x][y] = Field.SAND
            return True

def task1(data):
    area, source_x, source_y = data
    n = 0
    while simulate_and_place(area, source_x, source_y):
        n += 1
    return n


def task2(data):
    area, source_x, source_y = data
    for line in area:
        line.append(Field.EMPTY)
        line.append(Field.SOLID)
    # extend lines at the left and right
    area.append([Field.EMPTY for _ in range(len(area[0])-1)] + [Field.SOLID])
    area.append([Field.EMPTY for _ in range(len(area[0])-1)] + [Field.SOLID])
    new_area = [[Field.EMPTY for _ in range(len(area[0])-1)] + [Field.SOLID]
                for _ in range(2)]
    new_area.extend(area)
    area = new_area
    source_x += 2


    n = 0
    while area[source_x][source_y] == Field.SOURCE:
        if not simulate_and_place(area, source_x, source_y):
            for j in range(len(area[0])):
                print("".join(str(area[i][j]) for i in range(len(area))))
            assert False
        n += 1
        if area[1][-2] != Field.EMPTY:
            new_area = [[Field.EMPTY for _ in range(len(area[0])-1)] + [Field.SOLID]]
            new_area.extend(area)
            area = new_area
            source_x += 1
        if area[-2][-2] != Field.EMPTY:
            area.append([Field.EMPTY for _ in range(len(area[0])-1)] + [Field.SOLID])
    return n


def main():
    # fn = "input_bsp.txt"
    fn = "input.txt"
    t0 = perf_counter_ns()
    data = read_data(fn)
    check_data(data)
    t1 = perf_counter_ns()
    result1 = task1(deepcopy(data))
    t2 = perf_counter_ns()
    result2 = task2(data)
    t3 = perf_counter_ns()

    print(f"Data preprocessing in {format_ns(t1 - t0)}")
    print(f"Task 1: {result1} in {format_ns(t2 - t1)}")
    print(f"Task 2: {result2} in {format_ns(t3 - t2)}")


if __name__ == "__main__":
    main()
