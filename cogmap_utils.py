from utils import *

import numpy as np


def seqs_starts_to_binary_map(map_shape, seqs):
    binary_map = np.zeros(map_shape)
    for seq in seqs:
        point = seq[0]
        binary_map[point.y, point.x] = 1
    return binary_map


def get_coords_for_radius(center, radius):
    #|x|+|y|=radius ->  |y|=radius-|x|
    # x>0  -> y1 = radius-|x|
    if radius == 0:
        return [Point(center.x, center.y)]

    points = []
    for modx in range(0, radius+1):
        mody = radius - modx
        # x>0
        if modx != 0 and mody != 0:
            points.append(Point(modx + center.x, mody + center.y))
            points.append(Point(-modx + center.x, mody + center.y))
            points.append(Point(modx + center.x, -mody + center.y))
            points.append(Point(-modx + center.x, -mody + center.y))

        if modx == 0 and mody != 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(modx + center.x, -mody + center.y))

        if modx != 0 and mody == 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(-modx + center.x, mody + center.y))
    return points