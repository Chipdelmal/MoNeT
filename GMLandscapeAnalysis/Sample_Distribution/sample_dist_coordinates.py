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
import numpy as np
import pandas as pd

# Exponential or gamma?
EXP = True

# PARAMETERS TO EDIT
popnode = 15 # average population per node
cv = 0.8 # somewhat clustered compared to exponential
p = 0.15 # fraction of empty nodes
b = 90 # truncation upper bound
n_samp = 1 # how many times to resample from ZITE/ZITG
popconst = 15 # constant pop for second population

# PATH TO EDIT
folder = "simulations/"
filepath = "/Users/mayashen/Desktop/MoNeT/GMLandscapeAnalysis/Sample_Distribution/"+folder

poppath = "/Users/mayashen/Desktop/MoNeT/GMLandscapeAnalysis/Sample_Distribution/Yorkeys01_0001_I.csv"

os.path.exists(filepath)
if not os.path.exists(filepath):
    os.mkdir(folder)


def main():
    pops = pd.read_csv(poppath, header=0, index_col=0)
    # number of nodes in the network
    n = pops[pops['Cluster'] != 0].shape[0]
    n_const = pops.shape[0] - n
    pops = pops[['Latitude', 'Longitude']]

    if EXP:
        print("Sampling from truncated EXPONENTIAL distribution "+str(n_samp)+" times with "+str(n)+" nodes and size "+str(popnode)+" per node.")
        filename = "sample_exp_"+str(n).zfill(4)+"_"+str(popnode).zfill(4)+"_"+str(int(p*100)).zfill(3)+"_"+str(b).zfill(3)
        commandline_args = ['Rscript', '--vanilla', 'sample_exp.R']
        args = [str(n), str(popnode), str(p), str(b)]
    else:
        print("Sampling from truncated GAMMA distribution "+str(n_samp)+" times with "+str(n)+" nodes and size "+str(popnode)+" per node.")
        filename = "sample_gamm a_"+str(n).zfill(4)+"_"+str(popnode).zfill(4)+"_"+str(int(p*100)).zfill(3)+"_"+str(b).zfill(3)
        commandline_args = ['Rscript', '--vanilla', 'sample_gamma.R']
        args = [str(n), str(popnode), str(cv), str(p), str(b)]

    FNULL = open(os.devnull, 'w')
    for i in range(n_samp):
        # Call script to write population to csv
        csvfilepath = filepath+filename+"_"+str(i).zfill(3)+".csv"
        retcode = subprocess.call(commandline_args + [csvfilepath] + args, stdout=FNULL, stderr=subprocess.STDOUT)
        # Create csv with coordinates + second population
        pop_draws_df = pd.read_csv(csvfilepath, header=0)
        pop_draws = list(pop_draws_df.values.flatten()) + [popconst]*n_const
        pops_copy = pops.copy()
        pops_copy.insert(2, "n", pop_draws)
        pops_copy.to_csv(csvfilepath)
    print("Process completed.")

# RUN THIS
t0 = time.time()
main()
t1 = time.time()
print("Time: "+str(t1-t0))
