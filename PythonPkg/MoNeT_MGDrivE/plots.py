import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE.colors as monetPlots


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
    if style["legend"] is True:
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2,
                   ncol=2, borderaxespad=0.)
    ax.xaxis.set_label_text("")
    ax.yaxis.set_label_text("")
    # plt.ylabel("Allele Count")
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
    plt.ylabel("")
    plt.xlabel("")
    if style["legend"] is True:
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2,
                   ncol=2,  borderaxespad=0.)
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
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": monetPlots.cmaps}
):
    """
    Description:
        * Creates the heatmap plot of all the genotypes in the landscape
            separately.
    In:
        * landscapeData: population dynamics data
        * style: styling options for the plot
    Out:
        * fig: matplotlib figure
    Notes:
        * NA
    """
    genesNumber = len(geneSpatiotemporals["genotypes"])
    plotsList = [None] * genesNumber
    for i in range(0, genesNumber):
        plotsList[i] = plotGenotypeFromLandscape(
            geneSpatiotemporals["geneLandscape"][i],
            style={"aspect": style["aspect"], "cmap": style["cmap"][i]}
        )
    plotsDict = {
        "genotypes": geneSpatiotemporals["genotypes"],
        "plots": plotsList
    }
    return plotsDict


def plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": monetPlots.cmaps}
):
    """
    Description:
        * Plots the combined "landscape-heatmap" plots in one.
    In:
        * geneSpatiotemporals: Array of the spatiotemporal genotypes
            information (gene counts across nodes through time).
        * style: styling options for the plot
    Out:
        * fig: matplot fig of combined heatmaps
    Notes:
        * NA
    """
    alleleNames = geneSpatiotemporals["genotypes"]
    counts = geneSpatiotemporals["geneLandscape"]
    fig = plt.figure(figsize=(20, 5))
    for i in range(len(alleleNames)):
        plt.imshow(counts[i], cmap=style["cmap"][i], aspect=style["aspect"])
    return fig


def plotNodeDataRepetitions(
    nodeRepetitionsArray,
    style
):
    """
    Description:
        * Generates the "traces" plot for one node.
    In:
        * nodeRepetitionsArray: Intermediate structure generated by taking
            the information of a given node accross all landscapes.
        * style: styling options for the plot
    Out:
        * fig: matplotlib traces figure
    Notes:
        * This function is meant to work within plotLandscapeDataRepetitions,
            so it's not necessary to call it directly.
    """
    probeNode = nodeRepetitionsArray
    repsNumber = len(probeNode)
    genesNumber = len(probeNode[0][0])
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=style["aspect"])
    for j in range(0, repsNumber):
        transposed = probeNode[j].T
        for gene in range(0, genesNumber):
            ax.plot(
                transposed[gene],
                linewidth=style["width"],
                color=style["colors"][gene],
                alpha=style["alpha"]
            )
    return fig


def plotLandscapeDataRepetitions(
    landscapeReps,
    style
):
    """
    Description:
        * Generates the individual "traces" plots for a whole landscape.
    In:
        * landscapeReps: landscape repetitions data generated with
            loadAndAggregateLandscapeDataRepetitions.
        * style: styling options for the plot.
    Out:
        * figs: array of matplotlib traces figures.
    Notes:
        * NA
    """
    landscapes = landscapeReps["landscapes"]
    landscapesNumb = len(landscapeReps["landscapes"][0])
    figs = [None] * landscapesNumb
    for i in range(0, landscapesNumb):
        probeNode = zip(*landscapes)[i]
        figs[i] = plotNodeDataRepetitions(probeNode, style)
    return figs


def quickSaveFigure(fig, path):
    fig.savefig(path,
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
