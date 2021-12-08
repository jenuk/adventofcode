import copy

class Decrypt:
    combinations = (
        frozenset("ABCEFG"),  # 0 
        frozenset("CF"),      # 1 
        frozenset("ACDEG"),   # 2 
        frozenset("ACDFG"),   # 3 
        frozenset("BCDF"),    # 4 
        frozenset("ABDFG"),   # 5 
        frozenset("ABDEFG"),  # 6 
        frozenset("ACF"),     # 7 
        frozenset("ABCDEFG"), # 8
        frozenset("ABCDFG"),  # 9 
    )


    def __init__(self, inp, outp):
        self.nums = inp
        self.outp_code = outp
        self.solution = [None]*4
        self.letters = "abcdefg"
        self.possibilities = {x: set(self.letters.upper()) for x in self.letters}


    def solution_number(self):
        return int("".join(map(str, self.solution)))


    def test_number(self, code, number):
        def test(code, possibilities):
            # DFS to check if the number can be build by the possibilities
            if len(code) == 0:
                return True

            for segment in possibilities[code[0]]:
                if test(code[1:], {p: possibilities[p] - {segment} for p in possibilities}):
                    return True

            return False

        if len(code) != len(Decrypt.combinations[number]):
            return False

        possibilities = {
            x: self.possibilities[x] & Decrypt.combinations[number] for x in self.letters
        }

        if any(len(possibilities[k]) == 0 for k in code):
            return False

        code = sorted(code, key=lambda a: len(possibilities[a]))
        
        return test(code, possibilities)


    def check_code(self, code):
        segments = set()
        solutions = []
        for number, comb in enumerate(Decrypt.combinations):
            if self.test_number(code, number):
                solutions.append(number)
                segments |= Decrypt.combinations[number]

        for l in code:
            self.possibilities[l] &= segments

        return solutions


    def check_wires(self):
        # wire connects to single segment
        for wire in self.letters:
            if len(self.possibilities[wire]) != 1:
                continue

            for other in self.letters:
                if wire != other:
                    self.possibilities[other] -= self.possibilities[wire]

        # two wires connect to only two segments
        for wire1 in self.letters:
            if len(self.possibilities[wire1]) != 2:
                continue

            for wire2 in self.letters:
                if wire1 == wire2 or len(self.possibilities[wire2]) != 2:
                    continue
                if self.possibilities[wire1] != self.possibilities[wire2]:
                    continue

                for other in self.letters:
                    if other != wire1 and other != wire2:
                        self.possibilities[other] -= self.possibilities[wire1]


    def solve(self):
        while True:
            prev = copy.deepcopy(self.possibilities)
            for code in self.nums:
                s = self.check_code(code)
                if len(s) == 0:
                    raise ValueError(f"No option found for {code}")

            self.check_wires()

            for k, code in enumerate(self.outp_code):
                s = self.check_code(code)
                if len(s) == 0:
                    print(self.possibilities)
                    raise ValueError(f"No option found for {code}")
                elif len(s) == 1:
                    self.solution[k] = s[0]

            if all(x is not None for x in self.solution):
                break
            elif prev == self.possibilities:
                print(self.possibilities)
                print(self.nums, self.outp_code)
                print(self.solution)
                raise ValueError("Loop without improvement")



def read_data(filename):
    with open(filename) as file:
        content = file.readlines()
    content = [line.strip().split(" | ") for line in content]
    inp =  [line[0].split() for line in content]
    outp = [line[1].split() for line in content]

    return inp, outp


def task1(inp, outp):
    ls = map(len, (x for line in outp for x in line))
    result = sum(map(lambda x: x in {2, 3, 4, 7,}, ls))
    return result


def task2(inps, outps):
    res = 0
    for inp, outp in zip(inps, outps):
        d = Decrypt(inp, outp)
        d.solve()
        res += d.solution_number()

    return res



if __name__ == '__main__':
    inp, outp = read_data("input.txt")

    res1 = task1(inp, outp)
    res2 = task2(inp, outp)

    print(f"Task1: {res1}")
    print(f"Task2: {res2}")
