# https://ipython-books.github.io/131-simulating-a-discrete-time-markov-chain/

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Pop size, birth and death rate
N = 100
a = .5/N
b = .5/N

nsteps = 1000
x = np.zeros(nsteps)
x[0] = 25

for t in range(nsteps - 1):
    if 0 < x[t] < N - 1:
        # Is there a birth?
        birth = np.random.rand() <= a * x[t]
        # Is there a death?
        death = np.random.rand() <= b * x[t]
        # We update the population size.
        x[t + 1] = x[t] + 1 * birth - 1 * death
    # The evolution stops if we reach $0$ or $N$.
    else:
        x[t + 1] = x[t]

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.plot(x, lw=2)


ntrials = 100
x = np.random.randint(size=ntrials, low=0, high=N)
