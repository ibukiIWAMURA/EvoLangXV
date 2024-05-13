import os
import random

def generate_random_holistics(seed, n, data_path, zeros_size=1):
    random.seed(seed)
    assert 0 <= zeros_size <= 1
    n_zeros = int(n*zeros_size)
    n_ones = n - n_zeros
    assert 0 <= n_zeros <= 100
    assert 0 <= n_ones <= 100
    qspace_file = os.path.join(data_path, "query_space.txt")
    with open(qspace_file, "r") as f:
        query_lines = f.read().splitlines()
        query_zeros_space = [(q.split("\t")[0], int(q.split("\t")[1])) for q in query_lines if int(q.split("\t")[1])==0]
        query_ones_space = [(q.split("\t")[0], int(q.split("\t")[1])) for q in query_lines if int(q.split("\t")[1])==1]
    str_zeros_file = os.path.join(data_path, "string_space_0.txt")
    str_ones_file = os.path.join(data_path, "string_space_1.txt")
    with open(str_zeros_file, "r") as f:
        str_zeros_lines = f.read().splitlines()
        str_zeros = [str_zero_line for str_zero_line in str_zeros_lines]
    with open(str_ones_file, "r") as f:
        str_ones_lines = f.read().splitlines()
        str_ones = [str_one_line for str_one_line in str_ones_lines]

    random.shuffle(query_zeros_space)
    random.shuffle(query_ones_space)
    random.shuffle(str_zeros)
    random.shuffle(str_ones)

    query_zeros_samples = random.sample(query_zeros_space, n_zeros)
    str_zeros_samples = random.sample(str_zeros, n_zeros)
    holistic_zeros = [f"S/{q}/{c} -> {s}" for (q, c), s in zip(query_zeros_samples, str_zeros_samples)]

    query_ones_samples = random.sample(query_ones_space, n_ones)
    str_ones_samples = random.sample(str_ones, n_ones)
    holistic_ones = [f"S/{q}/{c} -> {s}" for (q, c), s in zip(query_ones_samples, str_ones_samples)]

    holistics = holistic_zeros + holistic_ones
    holistics_str = "\n".join(holistics)
    return holistics_str