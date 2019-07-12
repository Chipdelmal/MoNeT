import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import glob

pathRoot = "/Users/mayashen/Desktop/Marshall_Simulations/test/"

NUM_SWAP = 50
NUM_ITER = 5
NUM_NODES = 50
TIME = 1459
folderNames = monet.listDirectoriesInPath(pathRoot)
folderNames[0].split("_")

aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)

root = "/Users/mayashen/Desktop/repetitions_test/"
paths = [root+"swap_down_0_"+str(i)+"/ANALYZED/0001" for i in range(5)]
paths
test = monet.loadAndAggregateLandscapeDataRepetitions(paths, aggregationDictionary, True, True)
test.keys()
len(test["landscapes"])
len(test['landscapes'][0])
len(test['landscapes'][0][0])
len(test['landscapes'][0][0][0])
test['landscapes'][0][0][0]
test['genotypes'][3]

comp_data = []
for patch in range(52):
    comp_patch = []
    for row in range(1459):
        comp_row = np.zeros(4)
        for rep in range(5):
            comp_row += test['landscapes'][rep][patch][row]
        comp_patch.append(comp_row/5)
    comp_data.append(comp_patch)

comp_data = np.array(comp_data)

pd.DataFrame({'Time':range(1, 1460), 'W': comp_data[0][:,0], 'H': comp_data[0][:,1], 'R': comp_data[0][:,2], 'B': comp_data[0][:,3]}).to_csv("~/Desktop/test.csv", header=["Time", "W", "H", "R", "B"], index=None)
