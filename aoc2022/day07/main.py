from time import perf_counter_ns
from typing import Dict, List, Optional

# Ignore below

def format_ns(time: int) -> str:
    lengths = [1, 1000, 1000, 1000, 60, 60, 24]
    units = ["ns", "μs", "ms", "s", "minutes", "hours", "days"]
    idx = 1
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

class Node:
    def __init__(self, name: str, size: Optional[int]=None):
        self.name = name
        self.is_dir = size is None
        self._size = size
        self.children: Dict[str, Node] = dict()

    @property
    def size(self) -> int:
        if self._size is None:
            self._size = sum(c.size for c in self.children.values())
        return self._size

    def __str__(self, depth: int=0) -> str:
        dr = "dir" if self.is_dir else "file"
        res = " "*depth + f"- {self.name} ({dr}, {self.size})\n"
        for c in self.children.values():
            res += c.__str__(depth+1)
        return res


def process_data(content: str) -> Node:
    lines = content.split("\n")
    k = 0
    root = Node("/")
    current = root
    stack = []
    while (k < len(lines)):
        dl, cmd, *add = lines[k].split(" ")
        assert dl == "$"
        if cmd == "cd":
            assert len(add) == 1
            p = add[0]
            if p == "/":
                current = root
                stack = []
            elif p == "..":
                current = stack.pop()
            else:
                assert p in current.children
                stack.append(current)
                current = current.children[p]
                assert current.is_dir
            k += 1
        elif cmd == "ls":
            assert len(add) == 0
            k += 1
            while k < len(lines) and lines[k][0] != "$":
                typ, name = lines[k].split(" ")
                if typ == "dir":
                    node = Node(name)
                else:
                    node = Node(name, int(typ))
                current.children[name] = node
                k += 1
        else:
            raise RuntimeError(f"Unkown command {cmd}")
    return root


def check_data(data):
    pass


def find(node: Node, maxsize: int):
    if not node.is_dir:
        return []
    result = []
    if node.size <= maxsize:
        result.append(node)
    for c in node.children.values():
        result.extend(find(c, maxsize))
    return result


def task1(data: Node) -> int:
    dirs = find(data, 100000)
    return sum(d.size for d in dirs)


def task2(data: Node) -> int:
    total  = 70000000
    needed = 30000000
    available = total - data.size
    needed = needed - available
    stack = [data]
    best = data
    while len(stack) > 0:
        current = stack.pop()
        candidate_childs = False
        for child in current.children.values():
            if child.is_dir and child.size >= needed:
                stack.append(child)
                candidate_childs = True
        if not candidate_childs and current.size < best.size:
            best = current
    return best.size


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
