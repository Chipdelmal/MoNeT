import MoNeT_MGDrivE as monet
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

def plotNodeTraces(
    landscapeReps,
    style,
    figure
):
    """
    Description:
        * Generates the individual "traces" plot for a whole landscape.
    In:
        * landscapeReps: landscape repetitions data generated with
            loadAndAggregateLandscapeDataRepetitions.
        * style: styling options for the plot.
    Out:
        * fig: a matplotlib traces figure with all of the information on the landscapeReps.
    Notes:
        * NA
    """
    repetitions = len(landscapeReps["landscapes"])
    nodesNumb = len(landscapeReps["landscapes"][0])
    genesNumber = len(landscapeReps["landscapes"][0][0][0])

    if not figure:
        fig, ax = plt.subplots()
    else:
        fig = figure
        ax = figure.get_axes()[0]

    for rep in landscapeReps["landscapes"]:
        for node in rep:
            transposed = node.T
            for gene in range(0, genesNumber):
                ax.plot(
                    transposed[gene],
                    linewidth=style["width"],
                    color=style["colors"][gene],
                    alpha=style["alpha"]
                )

    return fig


colors = [
    "#090446", "#f20060", "#59ff00",
    "#ff28d4", "#6898ff", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)

styleT = {
    "width": 0.075, "alpha": .1, "dpi": 2*512, "legend": False,
    "aspect":0.02, "colors": colors, "format": "png",
    "xRange": [0, 9125], "yRange": [0, 50000]
}

pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys4/Experiment4/"
pathSet = pathRoot + "Yorkeys_AGG_*/"  # + "eRACR29"
foldersList = glob.glob(pathSet + "*GARBAGE")
sortedFolders = sorted(foldersList)

for folderElem in sortedFolders:
    # id = foldersList[j].split("/")[-1].split("_")[0]
    #clusteringNum = int(folderElem.split('_')[-1].split('/')[0])
    experimentList =  sorted(glob.glob(folderElem + "/E_*/"))
    aggStr = folderElem.split("/")[-2]
    for nameExp in experimentList:
        paths = monet.listDirectoriesWithPathWithinAPath(nameExp)
        aggregationDictionary = monet.autoGenerateGenotypesDictionary(
            ["W", "H", "E", "R", "B"],
            [
                'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
                'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
            ]
        )

        fig = None
        for repetition in paths:
            landRep = monet.loadAndAggregateLandscapeDataRepetitions(
                [repetition],
                aggregationDictionary,
                male=True,
                female=False,
            )
            singleNode = monet.sumAggregatedLandscapeDataRepetitions(landRep)

            fig = plotNodeTraces(singleNode, styleT, fig)

        fig.get_axes()[0].set_xlim(
          styleT["xRange"][0], styleT["xRange"][1]
        )
        fig.get_axes()[0].set_ylim(
          styleT["yRange"][0], styleT["yRange"][1]
        )
        fig.get_axes()[0].set_aspect(styleT["aspect"])
        monet.quickSaveFigure(
          fig,
          pathRoot + "/images2/garbage/" + aggStr +
          #nameExp.split("/")[-1] +
          "_G." + "png",
          dpi=styleT["dpi"],
          format="png"
        )
