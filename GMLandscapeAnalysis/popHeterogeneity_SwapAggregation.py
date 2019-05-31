import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

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

np.zeros(5)
for nameExp in folderNames[0:]:
    pathFull = pathRoot + nameExp
    filenames = monet.readExperimentFilenames(
            pathFull + "/ANALYZED/" + "0001/"
    )
    filenames['male'][0]
a        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        landscapeSumData['genotypes']
        hello = np.genfromtxt(
            filenames['male'][0],
            dtype=float,
            skip_header=1,
            delimiter=",",
            invalid_raise=False
        )
        hello
        df = pd.DataFrame(data=hello[0:, 1:], columns=landscapeSumData['genotypes'])
        df
        df[]
        df.to_csv("foo.csv")
        # aggData = monet.aggregateGenotypesInNode(
        #     landscapeSumData, aggregationDictionary
        # )
