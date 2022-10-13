from utils import *

import numpy as np


def seqs_starts_to_binary_map(map_shape, seqs):
    binary_map = np.zeros(map_shape)
    for seq in seqs:
        point = seq[0]
        binary_map[point.y, point.x] = 1
    return binary_map