import os
import aux
import numpy as np
import MoNeT_MGDrivE as monet


PAD = '\n' + 125 * '*' + '\n'
(CRED, CEND) = ('\033[91m', '\033[0m')
###############################################################################
# Style
###############################################################################
STYLE_HLT = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 2000], "yRange": [0, 20000],
        "colors": ['#9f00cc', '#ec0b43', '#0038a8']
    }
STYLE_HLT['aspect'] = monet.scaleAspect(.1, STYLE_HLT)

STYLE_ECO = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5, "xRange": [0, 2000], "yRange": [0, 1],
        "colors": [
                '#ff004d', '#80ff80', '#6600ff',
                '#e600ff', '#b3ccff', '#333380', '#f0a6ca'
            ]
    }
STYLE_ECO['aspect'] = monet.scaleAspect(.1, STYLE_ECO)


###############################################################################
# Functions Definitions
###############################################################################
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


def parseTitle(thresholds, prtcDays):
    title = '  '.join(['[{}: {}]'.format(
                str(round(1-x[0], 2)).ljust(4, '0'),
                str(x[1]).zfill(4)
            ) for x in zip(thresholds, prtcDays)]
        )
    return 'SUP: ' + title


def parseMinTitle(minTuple, SSPOP, thrs=.05):
    if(1 - minTuple[1] / SSPOP >= thrs):
        title = "MIN: [{}: {}]".format(
                int(minTuple[0]),
                round(1 - minTuple[1]/SSPOP, 2)
            )
    else:
        title = "MIN: [0: 0]"
    return title


def printTitle(ax, title):
    ax.text(
            .99, .95, title, color='Black', fontsize=2.5, alpha=.5,
            verticalalignment='top', horizontalalignment='right',
            transform=ax.transAxes
        )
    return ax


def printMinTitle(ax, title):
    ax.text(
            .99, .85, title, color='Red', fontsize=2.5, alpha=.5,
            verticalalignment='top', horizontalalignment='right',
            transform=ax.transAxes
        )
    return ax


def printVLines(ax, chngDays):
    for vLine in chngDays:
        ax.axvline(
                x=vLine, linewidth=.1,
                linestyle='--', color='Black', alpha=.5
            )
    return ax


def printMinLines(ax, minTuple, style, SSPOP, thrs=.05):
    if(1 - minTuple[1] / SSPOP >= thrs):
        ax.axhline(
                y=minTuple[1], xmin=0, xmax=minTuple[0]/style['xRange'][1],
                linewidth=.1, linestyle='--', color='Red', alpha=.5
            )
        ax.axvline(
                x=minTuple[0], ymin=0, ymax=minTuple[1]/style['yRange'][1],
                linewidth=.075, linestyle='--', color='Red', alpha=.5
            )
    return ax


def setRange(ax, style):
    ax.set_xlim(0, style['xRange'][1])
    ax.set_ylim(0, style['yRange'][1])
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
