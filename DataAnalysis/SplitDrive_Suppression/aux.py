import os
import aux
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

(SUP_COL, MIN_COL) = ('gray', 'red')
PAD = '\n' + 125 * '*' + '\n'
(CRED, CEND) = ('\033[91m', '\033[0m')
###############################################################################
# Style
###############################################################################
STYLE_HLT = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": 1,
        "xRange": [20, 1 * 365], "yRange": [0, 10500],
        "colors": [(.62, 0, .8, 0), (.93, .04, .26, .1), (0, .22, .66, 0)]
    }
STYLE_HLT['aspect'] = monet.scaleAspect(.25, STYLE_HLT)

STYLE_ECO = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 5 * 365], "yRange": [0, 1],
        "colors": [
                (255, 100, 100),  # Red
                (125, 255, 125),  # Light Green
                (100, 0, 255),  # Purple
                (230, 0, 255),  # Pink
                (180, 200, 254),  # Light Green
                (50, 50, 125),  # Dark Blue
                (250, 160, 200)   # Light Pink
            ]
    }
STYLE_ECO['aspect'] = monet.scaleAspect(.25, STYLE_ECO)
STYLE_ECO['colors'] = [(i[0]/255, i[1]/255, i[2]/255, .15) for i in STYLE_ECO['colors']]
STYLE_ECO['colors']

COLOR_SWATCH = [
        (149, 255, 68),  # Green
        (255, 105, 174),  # Pink
        (40, 42, 120),  # Blue
        (239, 33, 71),  # Red
        (255, 236, 0),  # Yellow
        (43, 132, 255),  # Gray
        (150, 99, 196),  # Purple
        (40, 40, 120),  # Pink (SD Ideal)
        (160, 100, 215) # Bright Green-Yellow (CRISPR Ideal)
    ]
COLORS = [
        [(.62, 0, .8, 0), (i[0]/255, i[1]/255, i[2]/255, .15), (0, .22, .66, 0)]
        for i in COLOR_SWATCH
    ]


###############################################################################
# Functions Definitions
###############################################################################
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
                color=style["colors"][gene]
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
        probeNode = list(zip(*landscapes))[i]
        figs[i] = plotNodeDataRepetitions(probeNode, style)
    return figs


def removeTicksAndLabels(axTemp):
    axTemp.set_xticklabels([])
    axTemp.set_yticklabels([])
    axTemp.set_xticks([])
    axTemp.set_yticks([])
    return axTemp


def getExperiments(PATH):
    dirs = sorted(next(os.walk(PATH))[1])
    temp = []
    for i in dirs:
        if(i != 'img'):
            temp.append(i)
    (expsNum, dirs) = (len(temp), temp)
    return (expsNum, dirs)


def selectAnalysisType(ECO, PATH_IMG):
    (PATH_HLT, PATH_ECO) = (PATH_IMG + 'hlt/', PATH_IMG + 'eco/')
    if ECO is True:
        (expType, style, path, doi) = ('ECO', aux.STYLE_ECO, PATH_ECO, 'W')
    else:
        (expType, style, path, doi) = ('HLT', aux.STYLE_HLT, PATH_HLT, 'Other')
    return (expType, style, path, doi)


def printHAxisNumbers(ax, numbers, xRange, color='Black', top=True, relStr=0):
    (yPos, vAlign) = (-.01, 'top')
    if top:
        (yPos, vAlign) = (1.01, 'bottom')
    # Plot text if the list is longer than one
    if len(numbers) > 0:
        for i in numbers:
            ax.text(
                    i/xRange, yPos, str(i-relStr), color=color, fontsize=4,
                    alpha=.5, verticalalignment=vAlign,
                    horizontalalignment='center', transform=ax.transAxes
                )
    return ax


def printHAxisNumbersAlt(ax, numbers, xRange, color='Black', relStr=0):
    if len(numbers) > 0:
        for (ix, i) in enumerate(numbers):
            (yPos, vAlign) = (-.01, 'top')
            # Alternate based on open/close of the threshold cross
            if ix < len(numbers) / 2:
                if (ix % 2 == 0):
                    (yPos, vAlign) = (1.01, 'bottom')
            else:
                if (ix % 2 != 0):
                    (yPos, vAlign) = (1.01, 'bottom')
            # Plot text
            ax.text(
                    i/xRange, yPos, str(i-relStr), color=color, fontsize=4,
                    alpha=.5, verticalalignment=vAlign,
                    horizontalalignment='center', transform=ax.transAxes
                )
    return ax


def printVAxisNumbers(ax, numbers, yRange, color='Black', left=True, rnd=True):
    (xPos, hAlign) = (-.004, 'right')
    if len(numbers) > 0:
        for i in numbers:
            if rnd:
                val = str(int(i))
            else:
                val = round(i, 2)
            #####
            ax.text(
                    xPos, i/yRange, val, color=color, fontsize=4,
                    alpha=.5, verticalalignment='center',
                    horizontalalignment=hAlign, transform=ax.transAxes
                )
    return ax


def parseTitle(thresholds, prtcDays):
    title = '  '.join(['[{}: {}]'.format(
                str(round(1-x[0], 2)).ljust(4, '0'),
                str(x[1]).zfill(4)
            ) for x in zip(thresholds, prtcDays)]
        )
    return 'SUP: ' + title


def parseMinTitle(minTuple, SSPOP, thrs=.05, relStr=0):
    if(1 - minTuple[1] / SSPOP >= thrs):
        title = "MIN: [{}: {}]".format(
                int(minTuple[0] - relStr),
                round(1 - minTuple[1]/SSPOP, 2)
            )
    else:
        title = "MIN: [0: 0]"
    return title


def printTitle(ax, title):
    ax.text(
            .999, .98, title, color=SUP_COL, fontsize=3, alpha=.75,
            verticalalignment='top', horizontalalignment='right',
            transform=ax.transAxes
        )
    return ax


def printMinTitle(ax, title):
    ax.text(
            .999, .01, title + ' ', color=MIN_COL, fontsize=3, alpha=.5,
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes
        )
    return ax


def getTimeToMinAtAllele(
            aggData,
            gIx,
            safety=.01
        ):
    """
    Description:
        * Calculates the point at which the total population reaches
            its minimum.
    In:
        * aggData: Genotypes aggregated data.
        * gIx: Gene-index of interest (column in the genotypes dictionary).
        * safety: Envelope of values around the steady state that are
            considered "stable" (as a proportion of the final total allele
            composition).
    Out:
        * time: Point in time at which the minimum is reached
        * popMin: Population size at its minimum
    """
    pop = [row[gIx] for row in aggData['population']]
    for time in range(len(pop)):
        popMin = min(pop)
        if np.isclose(pop[time], popMin, atol=safety):
            break
    return (time, popMin)
