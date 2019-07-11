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

for swap in range(NUM_SWAP + 1):
    outputpath = "/Users/mayashen/Desktop/Marshall_Simulations/swap_aggregated/swap_down_"+str(swap)+"/ANALYZED/0001/"
    for node in range(NUM_NODES):
        node_data = np.zeros(TIME)
        for iter in range(NUM_ITER):
            pathExp = "swap_down_"+str(swap)+"_"+str(iter)
            np.genfromtxt(
                pathRoot+pathExp,
                dtype=float,
                skip_header=1,
                delimiter=",",
                invalid_raise=False
            )

aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)

monet.readExperimentFilenames("/Users/mayashen/Desktop/swap_down_0_0/ANALYZED")
sexFilenameIdentifiers={"male": "ADM", "female": "AF1"}
"Users/mayashen/Desktop/swap_down_0_0/ANALYZED" + "/" + sexFilenameIdentifiers["male"] + "*.csv"

pd.read_csv("/Users/mayashen/Desktop/swap_down_0_0/ANALYZED/ADM_Mean_Patch0000.csv")
glob.glob("/Users/mayashen/Desktop/swap_down_0_0/ANALYZED/ADM_Mean_Patch0000.csv")

glob.glob("/Users/mayashen/Desktop/swap_down_0_0/ANALYZED/ADM*.csv")
loadLandscapeData(
    filenames, male=male, female=female, dataType=dataType
)
root = "/Users/mayashen/Desktop/repetitions_test/"
paths = [root+"swap_down_0_"+str(i)+"/ANALYZED/0001" for i in range(5)]
paths
test2 = monet.loadAndAggregateLandscapeDataRepetitions(paths, aggregationDictionary, True, True)
test.keys()
len(test["landscapes"])
len(test['landscapes'][0])
len(test['landscapes'][0][0])
len(test['landscapes'][0][0][0])
test['landscapes'][0][0][0]
test['genotypes']

test2.keys()
len(test2["landscapes"])
len(test2['landscapes'][0])
len(test2['landscapes'][0][0])
len(test2['landscapes'][0][0][0])
test2['landscapes'][0][0][0]
