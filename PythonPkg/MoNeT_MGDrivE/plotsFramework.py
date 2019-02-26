import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import MoNeT_MGDrivE.plots as monetPlots
from MoNeT_MGDrivE.experimentsHandler import getGenotypeArraysFromLandscape

def plotMeanGenotypeTrace(aggData, style):
    """
    Description:
        * Plots the mean response of an aggregate dataset.
    In:
        * aggData: dictionary containing "genotype" and "populations" pairs
        * style: dictionary containing width, colors, aspect, alpha
    Out:
        * fig: matplotlib figure
    Notes:
        * NA
    """
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df = pd.DataFrame(time, columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local = pd.DataFrame(pops, columns=groups)
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=style["aspect"])
    # plt.xticks([])
    # plt.yticks([])
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')
    for i in range(len(final)):
        final[i].plot(
            ax=ax, linewidth=style["width"], legend=False,
            color=style["colors"][i], alpha=style["alpha"]
        )
    legends = []
    for i in range(len(groups)):
        legends.append(
            mpatches.Patch(color=style["colors"][i], label=groups[i])
        )
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    ax.xaxis.set_label_text("")
    ax.yaxis.set_label_text("")
    plt.ylabel("Allele Count")
    return fig


def plotMeanGenotypeStack(aggData, style):
    """
    Description:
        * Plots the mean response of an aggregate dataset.
    In:
        * aggData: dictionary containing "genotype" and "populations" pairs
        * style: dictionary containing width, colors, aspect, alpha
    Out:
        * fig: matplotlib figure
    Notes:
        * NA
    """
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df = pd.DataFrame(time, columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local = pd.DataFrame(pops, columns=groups)
    fig, ax2 = plt.subplots()
    ax2.set_aspect(aspect=style["aspect"])
    allele_dict = {}
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')
    for i in range(len(groups)):
        allele_dict[groups[i]] = final[i].T.sum()
    res = pd.DataFrame(allele_dict)
    res = res.reindex(columns=groups)
    res.plot(
        kind='area', ax=ax2, legend=style["legend"], color=style["colors"],
        linewidth=style["width"], alpha=style["alpha"]
    )
    plt.ylabel("Allele Count")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    return fig


def plotGenotypeFromLandscape(
    landscapeGene,
    style={"aspect": 12, "cmap": monetPlots.cmaps[0]}
):
    """
    Description:
        * Creates the heatmap plot of a gene array
    In:
        * landscapeGene: spatiotemporal array for the gene to plot
        * style: styling options for the plot
    Out:
        * fig: matplotlib figure
    Notes:
        * NA
    """
    fig, ax = plt.subplots(nrows=1, figsize=(20, 5))
    ax.imshow(landscapeGene, cmap=style["cmap"], aspect=style["aspect"])
    return fig


def plotGenotypeArrayFromLandscape(
    landscapeData,
    style={"aspect": 12, "cmap": monetPlots.cmaps}
):
    """
    Description:
        * Creates the heatmap plot of all the genotypes in the landscape
    In:
        * landscapeData: population dynamics data
        * style: styling options for the plot
    Out:
        * fig: matplotlib figure
    Notes:
        * NA
    """
    genesNumber = len(landscapeData["genotypes"])
    plotsList = [None] * genesNumber
    for i in range(0, genesNumber):
        geneProbe = getGenotypeArraysFromLandscape(landscapeData)
        plotsList[i] = plotGenotypeFromLandscape(
            geneProbe["geneLandscape"][i],
            style={"aspect": style["aspect"], "cmap": style["cmap"][i]}
        )
    plotsDict = {"genotypes": landscapeData["genotypes"], "plots": plotsList}
    return plotsDict
