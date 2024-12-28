from typing import Iterator

from aoc_helper.utils import load_lines, ExclusiveTimeIt
from aoc_helper.graph import BaseNode, dfs

timeit = ExclusiveTimeIt()


@timeit
def prepare_input(
    lines: list[str],
) -> tuple[list[int], list[int]]:
    a = int(lines[0].split(" ")[-1])
    b = int(lines[1].split(" ")[-1])
    c = int(lines[2].split(" ")[-1])
    program = list(map(int, lines[-1].split(" ")[-1].split(",")))
    return [a, b, c], program


def eval_combo(op: int, register: list[int]):
    if op < 4:
        return op
    elif op == 7:
        raise ValueError("Reserved combo-op value")
    else:
        return register[op - 4]


@timeit
def task1(register: list[int], program: list[int]) -> str:
    output = ""
    instruction_pointer = 0
    while instruction_pointer < len(program) - 1:
        inst = program[instruction_pointer]
        op = program[instruction_pointer + 1]
        if inst == 0:
            register[0] >>= eval_combo(op, register)
        elif inst == 1:
            register[1] ^= op
        elif inst == 2:
            register[1] = eval_combo(op, register) & 0b111
        elif inst == 3:
            if register[0] != 0:
                instruction_pointer = op - 2
        elif inst == 4:
            register[1] ^= register[2]
        elif inst == 5:
            output += "," + str(eval_combo(op, register) & 0b111)
        elif inst == 6:
            register[1] = register[0] >> eval_combo(op, register)
        elif inst == 7:
            register[2] = register[0] >> eval_combo(op, register)
        else:
            raise ValueError(f"Illegal instruction {inst}")
        instruction_pointer += 2
    return output[1:]


class LineExecution(BaseNode):
    has_unique = True

    def __init__(self, pos: int, a: int, program: list[int], a_advance: int):
        self.pos = pos
        self.a = a
        self.program = program
        self.a_advance = a_advance

    def unique(self) -> tuple[int, int]:
        return (self.pos, self.a)

    def get_neighbors(self, reverse: bool = False) -> Iterator["LineExecution"]:
        assert not reverse
        if self.pos == -1:
            return

        for a_part in range(2**self.a_advance - 1, -1, -1):
            register = [(self.a << self.a_advance) + a_part, 0, 0]
            for inst_pointer in range(0, len(self.program) - 1, 2):
                inst = self.program[inst_pointer]
                op = self.program[inst_pointer + 1]

                if inst == 0:
                    register[0] >>= eval_combo(op, register)
                elif inst == 1:
                    register[1] ^= op
                elif inst == 2:
                    register[1] = eval_combo(op, register) & 0b111
                elif inst == 4:
                    register[1] ^= register[2]
                elif inst == 5:
                    if eval_combo(op, register) % 8 == self.program[self.pos]:
                        yield LineExecution(
                            self.pos - 1,
                            (self.a << self.a_advance) + a_part,
                            self.program,
                            self.a_advance,
                        )
                    break
                elif inst == 6:
                    register[1] = register[0] >> eval_combo(op, register)
                elif inst == 7:
                    register[2] = register[0] >> eval_combo(op, register)
                else:
                    raise ValueError(f"Illegal instruction {inst}")


@timeit
def task2(register: list[int], program: list[int]) -> int:
    result = 0
    instructions = [(program[k], program[k + 1]) for k in range(0, len(program) - 1, 2)]

    # these hold true for my input and the example; I expect these to be general
    # simplifications:
    # - the code has a single jump and jumps all to the beginning from the very end
    # - b and c are initialized only from a in every loop (e.g. previous b, c
    #   are overwritten)
    # - a is only shifted a constant, positive amount
    # - there is exactly one output
    had_output = False
    b_init = False
    c_init = False
    a_advance = 0
    for k, (inst, op) in enumerate(instructions):
        if inst == 3:
            assert k == len(instructions) - 1 and op == 0
        if inst == 5:
            assert not had_output
            had_output = True
        if inst == 0:
            assert op < 4
            a_advance += op
        if (not b_init) and (
            (inst == 2 or inst == 6) and (op < 5 or (op == 6 and c_init))
        ):
            b_init = True
        if (not c_init) and (inst == 7 and (op < 5 or (op == 5 and b_init))):
            c_init = True
        if inst == 4:
            assert b_init and c_init
        if inst == 1:
            assert b_init
        if inst in {0, 2, 5, 6, 7} and op > 4:
            assert [b_init, c_init][op - 4]
    assert had_output and a_advance > 0

    for node, _ in dfs(LineExecution(len(program) - 1, 0, program, a_advance)):
        if node.pos == -1:
            return node.a

    return result


def main(fn: str):
    lines = load_lines(fn)
    inp = prepare_input(lines)

    total_p1 = task1(*inp)
    total_p2 = task2(*inp)

    print(f"Task 1: {total_p1}")
    print(f"Task 2: {total_p2}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
