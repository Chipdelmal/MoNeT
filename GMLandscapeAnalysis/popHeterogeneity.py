import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math


def population_split(pop_size, n, C=0.0):
    """ Function to split population size into n groups with C randomness.
        pop_size: int, total population size
        n: int, number of groups to split pop_size
        C: int or float, can take on range of values from 0 (unif) to 1 (rand)
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


def array_creation(dist_apart, pop_size, n, C=0.0):
    """ Function that creates array of x coordinates, y coordinates, and
        populations (using population_split fn) along horizontal line (y coords
        = 0).
        dist_apart: int, distance between nodes
        pop_size: int, total population size
        n: int, number of groups to split pop_size
        C: int or float, can take on range of values from 0 (unif) to 1 (rand)
    """
    pop = np.array(population_split(pop_size, n, C))
    x_coords = np.linspace(0, dist_apart * (n + 1), n + 2)
    y_coords = np.zeros(n + 2)
    return np.array([x_coords, y_coords, pop])


def manual_array_creation(dist_apart, pop, dummy=False):
    """ Function that creates array of x coordinates, y coordinates, and
        populations (using given pop) along horizontal line (y coords = 0).
        dist_apart: int, distance between nodes
        pop: list, n population sizes
        dummy: boolean, default=False, whether or not to include dummy nodes at
        beginning and end of pop (dummy nodes have same value as the node after
        or before
        them).
    """
    n = len(pop)
    if dummy:
        pop.insert(0, pop[0])
        pop.append(pop[-1])
        x_coords = np.linspace(0, dist_apart * (n + 1), n + 2)
        y_coords = np.zeros(n + 2)
    else:
        x_coords = np.linspace(0, dist_apart * (n-1), n)
        y_coords = np.zeros(n)
    return np.array([x_coords, y_coords, pop])


def csv_creation(arr, file_name, VERT=True):
    """ Function that creates csv file from array of x coordinates, y
        coordinates, and populations. User may need to change path.
        arr: array, array of x coordinates, y coordinates, and populations
        file_name: string, name of file
        VERT: boolean, default=True, to create a vertical or horizontal csv
    """
    if VERT:
        pd.DataFrame({0: arr[0], 1: arr[1], 2: arr[2]}).to_csv("~/Desktop/popHeterog_csv/test/"+file_name+".csv", header=["x", "y", "n"], index=None)
    else:
        pd.DataFrame(arr).to_csv("~/Desktop/popHeterog_csv/"+file_name+".csv"".csv", header=None, index=None)


def setup(pop, n, type, base=10):
    """ Function that creates csv file from array of x coordinates, y
        coordinates, and populations. User may need to change path.
        arr: array, array of x coordinates, y coordinates, and populations
        file_name: string, name of file
        VERT: boolean, default=True, to create a vertical or horizontal csv
    """
    if type == "step_up" or type == "step_down":
        step = 2*(pop-(n*base))/((n-1)*n)
        pop_sizes = [round(base+(step*i)) for i in range(n)]
        if type == "step_up":
            return pop_sizes
        else:
            pop_sizes.reverse()
            return pop_sizes
    elif type == "up_down":
        if n % 2 == 0:  # even
            divide = (n-2)/2 * ((n-2)/2 + 1)
            step = (pop - n*base)/divide
            pop_sizes = [base+(step*i) for i in range(int(n/2))]
            pop_sizes_reverse = pop_sizes.copy()
            pop_sizes_reverse.reverse()
            pop_sizes.extend(pop_sizes_reverse)
            return pop_sizes
        else:  # odd
            divide = ((n-3)/2 * (n-1)/2) + ((n-1)/2)
            step = (pop - n*base)/divide
            peak = base+((n-1)*step/2)
            pop_sizes = [base+(step*i) for i in range(int((n-1)/2))]
            pop_sizes_reverse = pop_sizes.copy()
            pop_sizes_reverse.reverse()
            pop_sizes.append(peak)
            pop_sizes.extend(pop_sizes_reverse)
            return pop_sizes
    elif type == "down_up":
        if n % 2 == 0:  # even
            divide = (n-2)/2 * ((n-2)/2 + 1)
            step = (n*base - pop)/divide
            pop_sizes = [base+(step*i) for i in range(int(n/2))]
            if any(v <= 0 for v in pop_sizes):
                print("Base set too low, population becomes non-positive")
                return
            pop_sizes_reverse = pop_sizes.copy()
            pop_sizes_reverse.reverse()
            pop_sizes.extend(pop_sizes_reverse)
            return pop_sizes
        else:  # odd
            divide = ((n-3)/2 * (n-1)/2) + ((n-1)/2)
            step = (n*base - pop)/divide
            peak = base+((n-1)*step/2)
            pop_sizes = [base+(step*i) for i in range(int((n-1)/2))]
            pop_sizes_reverse = pop_sizes.copy()
            pop_sizes_reverse.reverse()
            pop_sizes.append(peak)
            if any(v <= 0 for v in pop_sizes):
                print("Base set too low, population becomes non-positive")
                return
            pop_sizes.extend(pop_sizes_reverse)
            return pop_sizes
    else:  # constant
        return [pop/n] * n


def swap(pops, n):
    """ Function that swaps the population nodes in an array n times.
        pops: list/array, list/array of population sizes
        n: int, number of times to swap two population nodes in pops
    """
    for _ in range(n):
        i, j = np.random.choice(range(len(pops)), 2)
        pops[i], pops[j] = pops[j], pops[i]
    return pops


# Script to manually create different population setups
plt.plot(range(50), swap(setup(30*50, 50, "step_down"), 4))


for i in range(51):
    for j in range(5):
        pop = swap(setup(30*50, 50, "step_down"), i)
        csv_creation(manual_array_creation(10, pop, len(pop)), "swap_down_"+str(i)+"_iter"+str(j))

pop = swap(setup(30*50, 50, "step_down"), 3)
csv_creation(manual_array_creation(10, pop, len(pop)), "swap_down_"+str(3)+"_iter"+str(1))


# Script to manually create different population setups
step_up = list(range(10, 211, 10))
sum(step_up)
step_down = step_up.copy()
step_down.reverse()
plt.figure()
plt.plot(range(21), step_down)
plt.xlabel('Node')
plt.ylabel('Population')
plt.savefig("step_down.png")

plt.figure()
plt.plot(range(21), step_up)
plt.xlabel('Node')
plt.ylabel('Population')
plt.savefig("step_up.png")

up = list(range(10, 211, 21))
down = up.copy()
down.reverse()
up_down = up.copy()
up_down.append(199+21)
up_down.extend(down)
sum(up_down)
plt.figure()
plt.plot(range(21), up_down)
sum(up_down)
plt.xlabel('Node')
plt.ylabel('Population')
plt.savefig("up_down.png")

up = list(range(21+17, 205, 17))
down = up.copy()
down.reverse()
down_up = down.copy()
down_up.append(21)
down_up.extend(up.copy())
sum(down_up)
plt.figure()
plt.plot(range(21), down_up)
plt.xlabel('Node')
plt.ylabel('Population')
plt.savefig("down_up.png")

sporadic = [50]*21
sum(sporadic)
sporadic[3] = sporadic[5]+55
sporadic[5] = sporadic[5]+100
sporadic[7] = sporadic[5]+150
sporadic[11] = sporadic[5]+180
sporadic[14] = sporadic[15]+100
sporadic[15] = sporadic[15]+142
sporadic[18] = sporadic[15]+200-9
sum(sporadic)
plt.figure()
plt.plot(range(21), sporadic)
plt.xlabel('Node')
plt.ylabel('Population')
plt.savefig("sporadic.png")

csv_creation(manual_array_creation(10, step_up, 21), "step_up")
csv_creation(manual_array_creation(10, step_down, 21), "step_down")
csv_creation(manual_array_creation(10, up_down, 21), "up_down")
csv_creation(manual_array_creation(10, down_up, 21), "down_up")
csv_creation(manual_array_creation(10, sporadic, 21), "sporadic")

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
