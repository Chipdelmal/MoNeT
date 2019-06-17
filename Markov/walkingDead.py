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
