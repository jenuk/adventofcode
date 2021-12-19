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

def make_rotations(scanner):
    # scanner: (B, 3)
    new = []
    for sign1, sign2, sign3 in itertools.product([-1, 1], repeat=3):
        for dim1 in {0, 1, 2}:
            for dim2 in {0, 1, 2} - {dim1}:
                for dim3 in {0, 1, 2} - {dim1, dim2}:
                    v = np.zeros_like(scanner)
                    v[:, 0] = sign1*scanner[:, dim1]
                    v[:, 1] = sign2*scanner[:, dim2]
                    v[:, 2] = sign3*scanner[:, dim3]
                    new.append(v)
    return np.stack(new)

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
    scanners = [make_rotations(x) for x in scanners]
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
