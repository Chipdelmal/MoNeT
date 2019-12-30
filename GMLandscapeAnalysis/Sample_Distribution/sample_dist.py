"""
Sample from truncated exponential/gamma distribution and write to csv files.
Script calls R files sample_exp.R and sample_gamma.R.

n: int, number of nodes in network
popnode: int, average population per node
cv: float, coefficient of variation (truncated gamma only)
p: float between 0 and 1, fraction of empty nodes
b: float, truncation upper bound
n_samp: int, number of samples to draw
"""

import os
import subprocess
import time
import pandas as pd

# Exponential or gamma?
EXP = True

# PARAMETERS TO EDIT
n = 50 # number of nodes in the network
popnode = 20 # average population per node
cv = 0.8 # somewhat clustered compared to exponential
p = 0.15 # fraction of empty nodes
b = 90 # truncation upper bound
n_samp = 10 # how many times to resample from ZITE/ZITG

# PATH TO EDIT
folder = "simulations/"
filepath = "/Users/sanchez.hmsc/Desktop/MoNeT/Sample/"+folder

os.path.exists(filepath)
if not os.path.exists(filepath):
    os.mkdir(folder)


def main():
    if EXP:
        print("Sampling from truncated EXPONENTIAL distribution "+str(n_samp)+" times with "+str(n)+" nodes and size "+str(popnode)+" per node.")
        filename = "sample_exp_"+str(n).zfill(4)+"_"+str(popnode).zfill(4)+"_"+str(int(p*100)).zfill(3)+"_"+str(b).zfill(3)
        commandline_args = ['Rscript', '--vanilla', 'sample_exp.R']
        args = [str(n), str(popnode), str(p), str(b)]
    else:
        print("Sampling from truncated GAMMA distribution "+str(n_samp)+" times with "+str(n)+" nodes and size "+str(popnode)+" per node.")
        filename = "sample_gamma_"+str(n).zfill(4)+"_"+str(popnode).zfill(4)+"_"+str(int(p*100)).zfill(3)+"_"+str(b).zfill(3)
        commandline_args = ['Rscript', '--vanilla', 'sample_gamma.R']
        args = [str(n), str(popnode), str(cv), str(p), str(b)]

    FNULL = open(os.devnull, 'w')
    for i in range(n_samp):
        csvfilepath = filepath+filename+"_"+str(i).zfill(3)+".csv"
        retcode = subprocess.call(commandline_args + [csvfilepath] + args, stdout=FNULL, stderr=subprocess.STDOUT)
        pop_draws = pd.read_csv(csvfilepath, header=0)
        pop_draws.columns = ['n']
        pop_draws.to_csv(csvfilepath, index=False)
    print("Process completed.")

# RUN THIS
t0 = time.time()
main()
t1 = time.time()
print("Time: "+str(t1-t0))
