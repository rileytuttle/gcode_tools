import numpy as np

def dist_between_two_points(p1, p2):
    # assumed to have to np arrays
    dist_vec = p1-p2
    dist = np.sqrt(np.sum(dist_vec**2))
    return dist
