import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import glob
import os


def combineSingleSwap(paths, outputpath, aggregationDictionary, male, female):
    """
    Description: This function combines a single set of repetition experiments
        and writes them to files.
    In:
        paths: list of strings, paths to folder containing repetitions to combine.
        outputpath: string, path to folder to write aggregated files.
        aggregationDictionary: matrix, genotypes and indices counts dictionary.
        male: boolean, True for male files, if male is True, female is false.
        female: boolean, True for female files, if female is True, male is false.
    """
    if not male and not female:
        raise Exception("No data was loaded. Check that at least one of the sexes is selected, and that the filenames list is not empty.")
    if male and female:
        raise Exception("Only one of male or female can be True.")
    aggData = monet.loadAndAggregateLandscapeDataRepetitions(paths, aggregationDictionary, male, female)
    num_paths = len(paths)
    num_patches = len(aggData['landscapes'][0])
    num_genotypes = len(aggData['genotypes'])
    time = len(aggData['landscapes'][0][0])
    comp_data = []
    for patch in range(num_patches):
        comp_patch = []
        for row in range(time):
            comp_row = np.zeros(num_genotypes)
            for rep in range(num_paths):
                comp_row += aggData['landscapes'][rep][patch][row]
            comp_patch.append(np.round(comp_row/num_paths, 2))
        comp_data.append(comp_patch)
    if male:
        names = ["ADM_Mean_Patch00"+'%02d' % i+".csv" for i in range(num_patches)]
    else:
        names = ["AF1_Mean_Patch00"+'%02d' % i+".csv" for i in range(num_patches)]
    comp_data = np.array(comp_data)
    for p in range(num_patches):
        df = pd.DataFrame({'Time': range(1, time + 1)})
        for g in range(len(aggData['genotypes'])):
            df[aggData['genotypes'][g]] = comp_data[p][:, g]
        if not os.path.isdir(outputpath+"/ANALYZED/0001/"):
            os.makedirs(outputpath+"/ANALYZED/0001/")
        df.to_csv(outputpath+"/ANALYZED/0001/"+names[p], header=['Time']+aggData['genotypes'], index=None)


def combineRepetitionData(paths, outputpaths, aggregationDictionary, male=True, female=True):
    """
    Description: This function combines multiple sets of repetition experiments
        and writes them to files.
    In:
        paths: list of lists of strings, each sublist is of paths to a folder
            containing repetitions to combine.
        outputpaths: list of strings, path to folder to write aggregated files.
        aggregationDictionary: matrix, genotypes and indices counts dictionary.
        male: boolean, True for male files.
        female: boolean, True for female files.
    """
    if not male and not female:
        raise Exception("No data was loaded. Check that at least one of the sexes is selected, and that the filenames list is not empty.")
    for p in range(len(paths)):
        if male:
            combineSingleSwap(paths[p], outputpaths[p], aggregationDictionary, True, False)
        if female:
            combineSingleSwap(paths[p], outputpaths[p], aggregationDictionary, False, True)


def pathGenerator(pathRoot, expName, numSwap, numRep, output=False):
    """
    Description: This function generates file paths to experiments to be passed
    into combineRepetitionData as paths argument.
    In:
        pathRoot: string, the root path of the experiments.
        expName: string, the experiment name.
        numSwap: int or array-like, if int: indicates that there are 1 to
            numSwap swaps, if array-like: array of swaps made.
        numRep: int, the number of repetitions of each swap.
        output: boolean, if True
    """
    paths = []
    if isinstance(numSwap, int):
        swaps = range(numSwap)
    else:
        swaps = numSwap
    for s in swaps:
        if not output:
            path = [pathRoot+expName+"_"+'%02d' % s+"_"+'%02d' % r+"/ANALYZED/0001" for r in range(numRep)]
            paths.append(path)
        else:
            paths.append(pathRoot+expName+"_"+'%02d' % s)
    return paths


aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)

combineRepetitionData(pathGenerator("/Users/mayashen/Desktop/Marshall_Simulations/test/", "swap_down", range(0, 51, 10), 20),
    pathGenerator("/Users/mayashen/Desktop/Marshall_Simulations/outputs/", "swap_down", range(0, 51, 10), 0, True), aggregationDictionary)


# SCRATCH WORK
root = "/Users/mayashen/Desktop/repetitions_test/"
paths = [root+"swap_down_0_"+str(i)+"/ANALYZED/0001" for i in range(5)]
paths
test = monet.loadAndAggregateLandscapeDataRepetitions(paths, aggregationDictionary, False, True)
test.keys()
len(test["landscapes"])
len(test['landscapes'][0])
len(test['landscapes'][0][0])
len(test['landscapes'][0][0][0])
test['landscapes'][0][0][0]
test['genotypes'][0]

comp_data = []
for patch in range(52):
    comp_patch = []
    for row in range(1459):
        comp_row = np.zeros(4)
        for rep in range(5):
            comp_row += test['landscapes'][rep][patch][row]
        comp_patch.append(np.round(comp_row/5, 2))
    comp_data.append(comp_patch)

comp_data = np.array(comp_data)

names = ["ADM_Mean_Patch000"+str(i)+".csv" for i in range(10)]
names.extend(["ADM_Mean_Patch00"+str(i)+".csv" for i in range(10, 52)])
names = ["AF1_Mean_Patch000"+str(i)+".csv" for i in range(10)]
names.extend(["AF1_Mean_Patch_00"+str(i)+".csv" for i in range(10, 52)])
names

for i in range(52):
    pd.DataFrame({'Time':range(1, 1460), 'W': comp_data[i][:, 0],
    'H': comp_data[i][:, 1], 'R': comp_data[i][:, 2],
    'B': comp_data[i][:, 3]}).to_csv(
    "~/Desktop/Marshall_Simulations/test_real/test_swap/ANALYZED/0001/"+names[i], header=["Time", "W", "H", "R", "B"],
    index=None)
comp_data[0][:, 0]
