import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet


def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='', vLines=[0, 0], hLines=[0]):
    figArr = monet.plotNodeTraces(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.axes.xaxis.set_visible(False)
    axTemp.axes.yaxis.set_visible(False)
    axTemp.xaxis.set_tick_params(width=1)
    axTemp.yaxis.set_tick_params(width=1)
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))

    if vLines[0] > 0:
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.2, facecolor='#3687ff', zorder=0)
    axTemp.axhline(
            hLines, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000'
        )
    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000')
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=0.05
        )
    plt.close('all')
    return True


def plotNodeDataRepetitions(
    nodeRepetitionsArray,
    style,
    xCord,
    yRange
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
    ax.plot([xCord, xCord], [0, yRange], 'k--', lw=.25)
    return fig


def plotLandscapeDataRepetitions(
    landscapeReps,
    style,
    xCord,
    yRange
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
        probeNode = list(zip(*landscapes))[i]
        figs[i] = plotNodeDataRepetitions(probeNode, style, xCord, yRange)
    return figs


def plotMeanGenotypeStack(
    aggData,
    style,
    xCord,
    yRange
):
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
    ax2.plot([xCord, xCord], [0, yRange], 'k--', lw=.5)
    # plt.ylabel("Allele Count")
    plt.xlabel("")
    if style["legend"] is True:
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2,
                   ncol=2,  borderaxespad=0.)
    return fig


def plotMeanGenotypeTrace(
    aggData,
    style,
    xCord,
    yRange
):
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
    ax.plot([xCord, xCord], [0, yRange], 'k--', lw=.25)
    ax.xaxis.set_label_text("")
    ax.yaxis.set_label_text("")
    # plt.ylabel("Allele Count")
    return fig
