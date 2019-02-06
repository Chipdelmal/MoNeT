import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def population_split(pop_size, n, C=0.0):
    # Hyperparameter C can range from 0.0: uniform to 1.0: random
    uniform_pop_size = ((pop_size * (1.0 - C)) // n) * n
    random_pop_size = pop_size - uniform_pop_size
    populations = [uniform_pop_size/n] * n
    random_pop = np.random.choice(range(n), int(random_pop_size))
    for i in random_pop:
        populations[i] += 1
    return populations


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
