import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


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
    pop = np.array(population_split(pop_size, n, C))
    x_coords = np.linspace(0, dist * (n + 1), n + 2)
    y_coords = np.zeros(n + 2)
    return np.array([x_coords, y_coords, pop])


def csv_creation(arr, file_name, VERT=True):
    if VERT:
        pd.DataFrame({0: arr[0], 1: arr[1], 2: arr[2]}).to_csv("popHeterog_csv/"+file_name+".csv", header=None, index=None)
    else:
        pd.DataFrame(arr).to_csv("popHeterog_csv/"+file_name+".csv"".csv", header=None, index=None)


for c in np.arange(0, 1.1, 0.1):
    csv_creation(array_creation(10, 2000, 20, c), str(int(c * 100)))

# Script to test function: ROUND 1
ACROSS_C = True
C_VAL = 1.0
num = 11
if ACROSS_C:
    vals = np.arange(0, 1.1, 0.1)
else:
    vals = range(1, num + 1)

pop_size = 100000
n = 1000
data = []
labels = []
for i in vals:
    if ACROSS_C:
        data.extend(population_split(pop_size, n, i))
    else:
        data.extend(population_split(pop_size, n, C_VAL))
    labels.extend([round(i, 1)] * n)
data_pd = pd.DataFrame({"group_size": data, "labels": labels})
plot1 = sns.violinplot(x="labels", y="group_size", data=data_pd)
plot1.set(xlabel='C values', ylabel='Node Population Size')
fig1 = plot1.get_figure()
fig1.savefig("popHeterog_1.png")

# Script to test function: ROUND 2
ACROSS_C = True
C_VAL = 1.0
num = 11
if ACROSS_C:
    vals = np.arange(0, 1.1, 0.1)
else:
    vals = range(1, num + 1)
iters = 1000
pop_size = 10000
n = 100
data = []
labels = []
for i in vals:
    for j in range(iters):
        if ACROSS_C:
            data.append(np.median(population_split(pop_size, n, i)))
        else:
            data.append(np.median(population_split(pop_size, n, C_VAL)))
    labels.extend([round(i, 1)] * iters)
data_pd = pd.DataFrame({"group_size": data, "labels": labels})
plot2 = sns.violinplot(x="labels", y="group_size", data=data_pd)
plot2.set(xlabel='C values', ylabel='Median Node Population Size: '+str(iters)+" Iterations")
fig2 = plot2.get_figure()
fig2.savefig("popHeterog_2.png")
