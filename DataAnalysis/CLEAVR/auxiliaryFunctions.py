import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet

def driveSelector(DRIVE):
    if DRIVE==1:
        id="CLEAVR"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W1", "W2", "H1", "B1", "B2", "R1"],
            [
                [0, 6, 12, 0, 1, 2, 6, 7, 8, 12, 13, 14],
                [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                [1, 3, 7, 9, 13, 15, 3, 4, 9, 10, 15, 16],
                [2, 4, 5, 8, 10, 11, 14, 16, 17, 5, 11, 17],
                [6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                    16, 17, 12, 13, 14, 15, 16, 17],
                []
            ]
        )
    elif DRIVE==2:
        id="CLEAVRX"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W1", "W2", "H1", "B1", "B2", "R1"],
            [
                [0, 6, 12, 18, 21, 24, 0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 21, 24],
                [0, 1, 2, 3, 4, 5, 18, 19, 20, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                 18, 19, 20, 21, 22, 23],
                [1, 3, 7, 9, 13, 15, 19, 22, 25, 3, 4, 9, 10, 15, 16, 19, 22, 25],
                [2, 4, 5, 8, 10, 11, 14, 16, 17, 20,
                    23, 26, 5, 11, 17, 20, 23, 26],
                [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26,
                 12, 13, 14, 15, 16, 17, 24, 25, 26],
                []
            ]
        )
    elif DRIVE==3:
        id="CRISPR"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W1", "W2", "H1", "B1", "B2", "R1"],
            [
                [0, 1, 2, 3, 0],
                [],
                [4, 5, 6, 1, 4],
                [9, 3, 6, 8, 9],
                [],
                [7, 8, 2, 5, 7]
            ]
        )
    elif DRIVE==4:
        id="CRISPRX"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W1", "W2", "H1", "B1", "B2", "R1"],
            [
                [0, 1, 2, 3, 0, 4],
                [],
                [4, 5, 6, 1, 4, 8],
                [9, 3, 6, 8, 9, 13],
                [],
                [7, 8, 2, 5, 7, 11]
            ]
        )
    return [id,aggregationDictionary]


def aggregateDataFromPath(path, aggregationDictionary):
    filenames = monet.readExperimentFilenames(path)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )
    aggData = monet.aggregateGenotypesInNode(landscapeSumData, aggregationDictionary)
    return aggData

def exportMeanPlotToDirectory(path,aggData,style):
    fig=monet.plotMeanGenotypeTrace(aggData, style)
    plt.xlim(0,style["xrange"])
    plt.ylim(0,style["yrange"])
    plt.savefig(path+"_T.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)
    return None

def exportStackedPlotToDirectory(path,aggData,style):
    fig=monet.plotMeanGenotypeStack(aggData, style)
    plt.xlim(0,style["xrange"])
    plt.ylim(0,style["yrange"])
    plt.savefig(path + "_S.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)
