import sys
import time
from collections import defaultdict
from functools import cmp_to_key

from einops import repeat, rearrange
import torch
from tqdm import tqdm

def read_and_split(filename):
    with open(filename, "r") as file:
        lines = file.read().rstrip().split("\n")

    splits = [[]]
    letters = {"w", "x", "y", "z"}
    for line in lines:
        command, *args = line.split(" ")

        if command == "inp":
            assert args[0] == "w"
            splits.append([])
            continue
        
        if args[1] in letters:
            splits[-1].append([command, *args])
        else:
            splits[-1].append([command, args[0], int(args[1])])

    assert len(splits[0]) == 0
    return splits[1:]


def alu(state, ops):
    key_to_coord = {"w": 0, "x": 1, "y": 2, "z": 3}
    for op in ops:
        if type(op[2]) is str:
            arg = state[key_to_coord[op[2]]]
        else:
            arg = op[2]

        if op[0] == "add":
            state[key_to_coord[op[1]]] += arg
        elif op[0] == "mul":
            state[key_to_coord[op[1]]] *= arg
        elif op[0] == "div":
            # state[key_to_coord[op[1]]].div_(arg, round_mode="trunc")
            state[key_to_coord[op[1]]] //= arg
        elif op[0] == "mod":
            state[key_to_coord[op[1]]] %= arg
        elif op[0] == "eql":
            state[key_to_coord[op[1]]] = (state[key_to_coord[op[1]]] == arg)
        else:
            raise ValueError(f"Unknown operation {op[0]}")
    return state

            
def main(splits):
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        if len(sys.argv) > 1:
            device = torch.device(f"cuda:{sys.argv[1]}")
        else:
            device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    # state: (w, x, y, z, min_number, max_number)
    state = torch.zeros((6, 1), dtype=torch.long, device=device)
    num_ins = 0

    for pos, ops in enumerate(tqdm(splits)):
        start_time = time.perf_counter()

        if True: # deduplicate before every inp
            # "naive" deduplicate (works better for me)
            state = state.cpu().T.tolist()

            # deduplicate
            state_dict = defaultdict(lambda: (float("inf"), float("-inf")))
            t_key = 0
            t_dict = 0
            for s in state:
                t0 = time.perf_counter()
                key = (s[1], s[2], s[3])
                t1 = time.perf_counter()
                tp = state_dict[key]
                state_dict[key] = (min(tp[0], s[4]), max(tp[1], s[5]))
                t2 = time.perf_counter()
                t_key += t1 - t0
                t_dict += t2 - t1
            print(f"Key {t_key:.2f}s\tDict {t_dict:.2f}s")

            # make state
            state = state[:len(state_dict)] # overwrite everything anyway
            for k, (key, val) in enumerate(state_dict.items()):
                state[k] = [0, *key, *val]
            state = torch.tensor(state, device=device, dtype=torch.long).T

            # # in-place deduplicate (doesn't work well somehow)
            # # sort
            # def cmp(i, j):
            #     a = state[[1,2,3], i] - state[[1,2,3], j]
            #     for nu in range(a.shape[0]):
            #         if a[nu] != 0:
            #             return 1 if a[nu] > 0 else -1
            #     return 0
            #
            # # tminus = time.perf_counter()
            # # a = state[[1,2,3]] # (3, n)
            # # diff = a.transpose(0,1)[..., None] - a[None, ...]
            # # cmp = ((diff > 0).int() - (diff < 0).int()).permute(1, 0, 2)
            # # cmp = torch.where(cmp[0] != 0, cmp[0],
            # #                   torch.where(cmp[1] != 1, cmp[1], cmp[2]))
            #
            # t0 = time.perf_counter()
            # inds = list(range(state.shape[1]))
            # inds.sort(key = cmp_to_key(cmp))
            # t1 = time.perf_counter()
            #
            # base_idx = inds[0]
            # mini = state[4, base_idx]
            # maxi = state[5, base_idx]
            # keep = [base_idx]
            # mins = []
            # maxs = []
            # for idx in inds[1:]:
            #     if cmp(idx, base_idx) == 0:
            #         mini = min(mini, state[4, idx])
            #         maxi = min(maxi, state[5, idx])
            #     else:
            #         mins.append(mini)
            #         maxs.append(maxi)
            #         keep.append(idx)
            #         mini = state[4, base_idx]
            #         maxi = state[5, base_idx]
            # t2 = time.perf_counter()
            #
            # state = state[:, keep]
            # state[4, :] = torch.tensor(mini)
            # state[5, :] = torch.tensor(maxi)
            #
            # t3 = time.perf_counter()
            # print(
            #     # f"Precomp: {t0-tmius:.2f}s",
            #     f"Sort: {t1-t0:.2f}s",
            #     f"Iterate: {t2-t1:.2f}s",
            #     f"Reduce: {t3-t2:.2f}s",
            #     sep="\n")

        # reduplicate
        state = repeat(state, "k n -> k n 9")
        state[0, :, :] = torch.arange(1,10, device=device)[None, :]
        state = rearrange(state, "k n m -> k (n m)")

        # update monad number
        state[4] = state[4]*10 + state[0]
        state[5] = state[5]*10 + state[0]
        mid_time = time.perf_counter()

        state = alu(state, ops)
        num_ins += len(ops)+1
        end_time = time.perf_counter()
        print(f"Deduplication {mid_time - start_time:.4f}s",
              f"Instructions {end_time - mid_time:.4f}s", sep="\n")
        print(state.shape[1], num_ins)

    valid = (state[3, :] == 0)
    state = state[:, valid]
    return torch.min(state[4]), torch.max(state[5])
    

if __name__ == '__main__':
    splits = read_and_split("input.txt")

    start_time = time.perf_counter()
    res2, res1 = main(splits) 
    end_time   = time.perf_counter()

    print(f"Elapsed time: {end_time - start_time:.3f} seconds")
    print(f"Result 1: {res1}")
    print(f"Result 2: {res2}")
