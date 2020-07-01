#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import numpy as np
import operator as op
from glob import glob
# import compress_pickle as pkl
from functools import reduce
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


def flatten(l):
    return reduce(lambda x, y: x+y, l)


def filterFromName(df, id, header):
    fltr = [True] * len(df)
    for ix in range(len(id)):
        fltr = fltr & (df[header[ix]] == id[ix])
    return fltr


def getXpId(pFile, idIx):
    splitXpId = re.split('_|-', pFile.split('/')[-1].split('.')[-2])
    xpId = [int(splitXpId[i]) for i in idIx]
    return xpId


def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, title):
    print(monet.PAD)
    (cred, cwht, cend) = (monet.CRED, monet.CWHT, monet.CEND)
    print(cwht+'UCI '+title+' ['+str(time)+']'+cend)
    print(monet.PAD)
    print('{}* Root: {}{}'.format(cred, PATH_ROOT, cend))
    print('{}* Imgs: {}{}'.format(cred, PATH_IMG, cend))
    print('{}* Data: {}{}'.format(cred, PATH_DATA, cend))
    print(monet.PAD)


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'GARBAGE/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


def splitExpNames(PATH_OUT, ext='lzma'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='', vLines=[0]):
    figArr = monet.plotLandscapeDataRepetitions(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.vlines(
            vLines, 0, 1,
            transform=axTemp.get_xaxis_transform(),
            colors='#FF007FA0',
            linestyles='dashed', linewidth=.25
        )
    # axTemp.set_xticks(range(0, STYLE["xRange"][1], 150))
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}-{}.png".format(PATH_IMG, nS, append),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')
    return True


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.lzma'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


###############################################################################
# Preprocess Data
###############################################################################
def calcQuantWOP(srpPrb, meanRef, thresholds, gIx, quantile=.95):
    """
    Calculates the mean window of protection for the quantile response of two
        populations.
    Args:
        srpPrb (dict): SRP population of the probe population.
        meanRef (np.array): Mean population of the reference population
        thresholds (list): List of ratios to use as thresholds.
        gIx (int): Index of the genotype of interest's location
        quantile (float): Quantile for the thresholds calculation
        cmprOp(function): Operation to compare against (less than, greater
            than, etcetera).
    Returns:
        list: Returns the time at which the condition is met at a given
            quantile level.
    """
    prb = srpPrb['landscapes']
    smpNum = len(prb)
    (wopArr, ttiArr, ttoArr) = [
            np.empty((smpNum, len(thresholds))) for i in range(3)
        ]
    for s in range(smpNum):
        refPop = meanRef['population']
        ratioOI = monet.getPopRatio(prb[s], refPop, gIx)
        thsArray = monet.comparePopToThresh(ratioOI, thresholds, cmprOp=op.lt)
        thsDays = monet.thresholdMet(thsArray)
        wopArr[s] = [len(i) for i in thsDays]
        ttiArr[s] = [min(i) for i in thsDays]
        ttoArr[s] = [max(i) for i in thsDays]
    (quantWOP, quantTTI, quantTTO) = [
            np.nanquantile(i, quantile, axis=0) for i in [wopArr, ttiArr, ttoArr]
        ]
    return (quantWOP, quantTTI, quantTTO)
