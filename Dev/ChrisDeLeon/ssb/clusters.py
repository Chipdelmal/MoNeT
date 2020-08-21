# MULTIPROCESS CLUSTERING SCRIPT

from collections import defaultdict
import multiprocessing as mp
import getopt
import pickle
import sys
import os

# Custom Libraries
import mpc_defs

def parse(argv):
    
    opts, args = getopt.getopt(argv, "l:k:o:c:n:e:")
    
    loctn = None # Path to locations CSV file
    kernl = None # Path to a directory of kernels (all as CSV files)
    o_dir = None # The directory to store outputs (default is 'outputs')
    cnums = None # The clusters to use. Formatted as a comma separated string of numbers: '1,2,3,...'
    procs = None # The number of processes (if unspecified then the number returned by cpu_count() is used)
    expid = None # The experiment id (used for naming the output .pkl file)
    
    for opt, arg in opts:
        if opt in ['-l']:
            loctn = arg
        elif opt in ['-k']:
            kernl = arg
        elif opt in ['-o']:
            o_dir = arg
        elif opt in ['-c']:
            cnums = list(map(int, arg.replace(' ', '').split(',')))
        elif opt in ['-n']:
            procs = int(arg)
        elif opt in ['-e']:
            expid = arg
        else: pass
    
    if o_dir is None:
        if not os.path.exists('outputs'):
            os.mkdir('outputs')
        o_dir = 'outputs'  
    
    if expid is None:
        expid = 0
    
    if any(map(lambda x: x is None, [loctn, kernl, cnums])):
        raise ValueError
    else:
        return loctn, kernl, o_dir, cnums, procs, expid

def get_inputs(loctn, kernl, cnums):
    inputs = []
    for k in os.listdir(kernl):
        name = k.split('.')[0]
        for c in cnums:
            inputs.append((name, os.path.join(kernl, k), loctn, c))
    return inputs

if __name__ == "__main__":
    
    # Gather inputs for experiments
    try:
        loctn, kernl, o_dir, cnums, procs, expid = parse(sys.argv[1:])
    except (getopt.GetoptError, ValueError) as e:
        print('Error collecting inputs:\n\n', e)
        sys.exit()
    
    # Format inputs for multiprocessing
    inputs = get_inputs(loctn, kernl, cnums)
    
    # Perform multiprocessing
    results = []
    print("\nProcessing inputs...\t", end='')
    sys.stdout.flush()
    with mp.Pool(processes=procs) as pool:
        results = pool.starmap(mpc_defs.experiment, inputs)
    print("Done!")
    
    # Load results into a more organized format
    outputs = defaultdict(dict)
    for n, c, d in results:
        outputs[c][n] = d
        
    # Store results
    with open('{}/outputs_exp{}.pkl'.format(o_dir, expid), 'wb') as output:
        pickle.dump(outputs, output, pickle.HIGHEST_PROTOCOL)
