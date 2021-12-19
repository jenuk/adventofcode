from collections import defaultdict
import itertools
import re

import numpy as np

def read_scanners(filename):
    with open(filename) as file:
        content = file.read()

    scanners = re.split("--- scanner \\d+ ---\n", content)[1:]
    for k, x in enumerate(scanners):
        scanners[k] = np.array([list(map(int, a.split(","))) for a in x.strip().split("\n")])

    return scanners


def gen_rotation_matrices():
    matrices = [
        # identity
        np.array([[ 1, 0, 0], [ 0, 1, 0], [ 0, 0, 1]]),
        # x-rotation
        np.array([[ 1, 0, 0], [ 0, 0,-1], [ 0, 1, 0]]),
        # y-rotation
        np.array([[ 0, 0, 1], [ 0, 1, 0], [-1, 0, 0]]),
        # z-rotation
        np.array([[ 0,-1, 0], [ 1, 0, 0], [ 0, 0, 1]]),
    ]

    for _ in range(3):
        for a in matrices:
            for b in matrices:
                x = a @ b
                if not any(map(lambda u: np.all(u == x), matrices)):
                    matrices.append(x)

    return np.stack(matrices) # (24, 3, 3)


def rotate(scanner, rotations):
    # scanner (B, 3)
    # rotations (24, 3, 3)
    # add dimensions to make broadcasting work
    return (rotations[:, None, :, :] @ scanner[None, :, :, None]).squeeze(3)


def find_overlap(sc1, sc2):
    # assume sc1: [1, B1, 3]
    # assume sc1: [R, B2, 3]

    diffs = sc1[:, None, :, :] - sc2[:, :, None, :]
    # gives [R, B1, B2, 3]
    for k in range(diffs.shape[0]):
        counts = defaultdict(int)
        for i in range(diffs.shape[1]):
            for j in range(diffs.shape[2]):
                counts[tuple(diffs[k, i, j])] += 1
        for vec, c in counts.items():
            if c >= 12:
                return np.array(vec), k

    return None, None


def calc_overlap(scanners):
    found = [(0, np.array([0, 0, 0]), 0)]
    done = {0}

    i = 0
    while (i < len(found)):
        print(found[i])
        idx, offset, rot = found[i]
        sc = scanners[idx][rot:rot+1] + offset

        for j in range(len(scanners)):
            if j in done:
                continue
            
            vec, k = find_overlap(sc, scanners[j])
            if vec is None:
                continue

            found.append((j, vec, k))
            done.add(j)

        i += 1

    return found


if __name__ == '__main__':
    scanners = read_scanners("input.txt")
    rotations = gen_rotation_matrices()
    scanners = [rotate(sc, rotations) for sc in scanners]
    solution = calc_overlap(scanners)
    
    vecs = set()
    for idx, offset, rot in solution:
        sc = scanners[idx][rot] + offset
        for k in range(sc.shape[0]):
            vecs.add(tuple(sc[k]))
    print("Task1", len(vecs))


    maxi = 0
    for _, offset1, _ in solution:
        for _, offset2, _ in solution:
            maxi = max(maxi, np.linalg.norm(offset1 - offset2, ord=1)) 
    print("Task2", maxi)
