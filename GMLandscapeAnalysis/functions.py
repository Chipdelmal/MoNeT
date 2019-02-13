
import numpy as np


def population_split(pop_size, n, C=0.0):
    """ Function to split population size into n groups.
        pop_size: int, total population size
        n: int, number of groups to split pop_size
        C: int or float, can take on range of values from 0 (uniform) to 1 (random).
    """
    uniform_pop_size = ((pop_size * (1.0 - C)) // n) * n
    random_pop_size = pop_size - uniform_pop_size
    populations = [uniform_pop_size/n] * n
    random_pop = np.random.choice(range(n), int(random_pop_size))
    for i in random_pop:
        populations[i] += 1
    base = pop_size / n
    populations.insert(0, base)
    populations.append(base)
    return populations


def array_creation(dist, pop_size, n, C=0.0):
    """
    Inputs:
    dist: int or float, step size in x-coordinate
    pop_size: int, total population size
    n: int, number of groups to split pop_size
    C: int or float, can take on range of values from 0 (uniform) to 1 (random).

    Returns
    Array of arrays containing the coordinates and population count
    """
    pop = np.array(population_split(pop_size, n, C))
    x_coords = np.linspace(0, dist * (n + 1), n + 2)
    y_coords = np.zeros(n + 2)
    return np.array([x_coords, y_coords, pop])
