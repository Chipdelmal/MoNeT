from random import random
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats
import math
import copy

def gaussian_cluster(n, p, v, x1=0, x2=1):
    """
    n: int, number of total points
    p: int, number of points to perturb
    v: float or int, variance of noise term, N(0, v)
    x1: float or int, lower bound on line
    x2: float or int, upper bound on line
    """
    base = np.linspace(x1, x2, n)
    if v == 0:
        return base
    #randomly sample from base to pick p points to perturb
    index = np.sort(np.random.choice(base.shape[0], p, replace=False))
    perturb = base[index]
    #perturb p points
    noise = stats.norm.rvs(loc=0, scale=v, size=len(perturb), random_state=21)
    #modulo the noise to keep within range
    perturbed = (perturb + noise)%10
    #add new points to base to make new pointset
    new_points = copy.deepcopy(base)
    new_points[index] = perturbed
    return new_points

test_base = gaussian_cluster(50, 25, 0)
plt.scatter(test_base, np.zeros((len(test_base))),alpha=0.5)

test_cluster = gaussian_cluster(50, 25, 5)
plt.scatter(test_cluster, np.zeros((len(test_cluster))),alpha=0.5)
