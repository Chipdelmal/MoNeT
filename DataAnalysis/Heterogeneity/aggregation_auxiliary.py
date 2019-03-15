import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import MoNeT_MGDrivE as monetPlots

def calculateMaxPopulationInLandscape(landscapeReps):
    landscapes = landscapeReps["landscapes"]
    list = [None] * len(landscapeReps["landscapes"][0])
    for i in range(len(landscapeReps["landscapes"][0])):
            list[i] = sum(landscapes[0][i][0])
    return max(list)


def plotMeanGenotypeStack(
    aggData,
    style,
    vLinesCoords=[]
):
    """
    Description:
        * Plots the mean response of an aggregate dataset.
    In:
        * aggData: dictionary containing "genotype" and "populations" pairs
        * style: dictionary containing width, colors, aspect, alpha
        * lineCoords
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
    for i in range(len(vLinesCoords)):
        ax2.plot(
            [vLinesCoords[i], vLinesCoords[i]],
            [style["yRange"][0], style["yRange"][1]],
            'k--',
            lw=.5
        )
    # plt.ylabel("Allele Count")
    plt.xlabel("")
    if style["legend"] is True:
        plt.legend(
            bbox_to_anchor=(1.05, 1), loc=2,
            ncol=2,  borderaxespad=0.
        )
    return fig


def plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": monetPlots.cmaps},
    vmin=None,
    vmax=None
):
    """
    Description:
        * Plots the combined "landscape-heatmap" plots in one.
    In:
        * geneSpatiotemporals: Array of the spatiotemporal genotypes
            information (gene counts across nodes through time).
        * style: styling options for the plot
        * vmin:
        * vmax:
    Out:
        * fig: matplot fig of combined heatmaps
    Notes:
        * NA
    """
    alleleNames = geneSpatiotemporals["genotypes"]
    counts = geneSpatiotemporals["geneLandscape"]
    fig = plt.figure(figsize=(20, 5))
    for i in range(len(alleleNames)):
        plt.imshow(
            counts[i],
            cmap=style["cmap"][i],
            aspect=style["aspect"],
            vmin=vmin, vmax=vmax
        )
    return fig
