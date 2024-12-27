from typing import Callable


def scalar_vec(scalar: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(scalar * x for x in vector)


def vec_op(
    vector_a: tuple[int, ...], vector_b: tuple[int, ...], op: Callable[[int, int], int]
) -> tuple[int, ...]:
    return tuple(op(a, b) for a, b in zip(vector_a, vector_b))
