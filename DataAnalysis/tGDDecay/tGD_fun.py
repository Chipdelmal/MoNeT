#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import numpy as np
import operator as op
from glob import glob
import compress_pickle as pkl
from functools import reduce
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['axes.linewidth'] = 1


def getFilteredFiles(filterGlobPattern, unfilteredGlobPattern):
    filterSet = set(glob(filterGlobPattern))
    fullSet = set(glob(unfilteredGlobPattern))
    filteredList = sorted(list(fullSet - filterSet))
    return filteredList


def flatten(l):
    return reduce(lambda x, y: x+y, l)


def filterFromName(df, id):
    header = list(df.columns)
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


def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='', vLines=[0, 0]):
    figArr = monet.plotLandscapeDataRepetitions(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.xaxis.set_tick_params(width=1)
    axTemp.yaxis.set_tick_params(width=1)
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.25, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.25, color=(0, 0, 0))
    axTemp.axvspan(vLines[0], vLines[1], alpha=0.2, facecolor='#3687ff', zorder=0)
    #axTemp.vlines(
    #        vLines, 0, 1, alpha=0,
    #        transform=axTemp.get_xaxis_transform(),
    #        colors='#3687ff',  # '#FF007FA5'
    #        linestyles='-', linewidth=1, zorder=0
    #    )
    # axTemp.set_xticks(range(0, STYLE["xRange"][1], 150))
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=.05
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
# Postprocess Data
###############################################################################
def calcQuantMetrics(
            srpPrb, meanRef, ssRef,
            thresholds, gIx, hIx,
            quantile=.95, ssTolerance=.05
        ):
    prb = srpPrb['landscapes']
    smpNum = len(prb)
    (wopArr, ttiArr, ttoArr, ttsArr) = [
            np.empty((smpNum, len(thresholds))) for i in range(4)
        ]
    (ttsArr, qasArr) = (np.empty((smpNum, 1)), np.empty((smpNum, 1)))
    for s in range(smpNum):
        # TTI, TTO, WOP -------------------------------------------------------
        refPop = meanRef['population']
        ratioOI = monet.getPopRatio(prb[s], refPop, gIx)
        thsArray = monet.comparePopToThresh(ratioOI, thresholds, cmprOp=op.lt)
        thsDays = monet.thresholdMet(thsArray)
        wopArr[s] = [len(i) for i in thsDays]
        ttiArr[s] = [min(i) for i in thsDays]
        ttoArr[s] = [max(i) for i in thsDays]
        # TTS -----------------------------------------------------------------
        for i in range(len(prb)):
            # Get the population to analyze and its final value from the mean
            pIx = [i[gIx] for i in prb[i]]
            hLast = prb[i][-1][hIx]
            ssVal = ssRef['population'][-1][gIx]
            # Calculate the tolerance from the total population
            tolPop = refPop[-1][-1]*(ssTolerance)
            # Calculate the envelope
            lThan = monet.comparePopToThresh(pIx, [ssVal+tolPop], cmprOp=op.lt)
            gThan = monet.comparePopToThresh(pIx, [ssVal-tolPop], cmprOp=op.gt)
            ssDays = [(i[0] and i[1]) for i in zip(lThan, gThan)]
            # Get the first break of the envelope (Beware!)
            ssDaysIx = monet.thresholdMet(ssDays)[-1]
            # ssDaysIx.reverse()
            ssFirst = [ssDaysIx[0]]     # [fstNonConsecutive(ssDaysIx)]
            ttsArr[i] = ssFirst
            qasArr[i] = hLast
    # print('{}:{} '.format(ssDaysIx, ssFirst))
    outArr = [wopArr, ttiArr, ttoArr]
    # Return arrays -----------------------------------------------------------
    (quantWOP, quantTTI, quantTTO) = [
            np.nanquantile(i, quantile, axis=0) for i in outArr
        ]
    quantTTS = [
            np.nanquantile(ttsArr, quantile), np.nanquantile(qasArr, quantile)
        ]
    return (quantWOP, quantTTI, quantTTO, quantTTS)


def longConsecutive(s):
    rl = {}
    best_range = range(0)
    for x in s:
        run = rl[x] = rl.get(x-1, 0) + 1
        r = range(x-run+1, x+1)
        if len(r) > len(best_range):
            best_range = r
    return list(best_range)


def first_consecutive(lst):
    day = lst[0]
    for (i, j) in enumerate(lst, lst[0]):
        if (day-i) != j:
            return j


def fstNonConsecutive(arr):
    seed = arr.pop(0)
    for num in arr:
        seed = seed - 1
        if num != seed:
            return seed + 1
    return 0

###############################################################################
# Save Figure
###############################################################################
def quickSaveFig(filename, fig):
    fig.savefig(
         filename,
         dpi=750, facecolor=None, edgecolor='w',
         orientation='portrait', papertype=None, format='png',
         transparent=True, bbox_inches='tight', pad_inches=.01
     )
