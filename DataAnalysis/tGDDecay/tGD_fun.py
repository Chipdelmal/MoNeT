#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import numpy as np
import pandas as pd
import tGD_aux as aux
import operator as op
from glob import glob
import matplotlib as mpl
from functools import reduce
import MoNeT_MGDrivE as monet
from scipy.interpolate import griddata

###############################################################################
# Globals
###############################################################################
(NDX, NDY) = (1000, 1000)
mpl.rcParams['axes.linewidth'] = 1


###############################################################################
# Response Surface
###############################################################################
def calcResponseSurface(iX, iY, dZ, scalers=(1, 1, 1), mthd='linear'):
    (xN, yN, zN) = (
            np.array([float(i/scalers[0]) for i in iX]),
            np.array([float(i/scalers[1]) for i in iY]),
            np.array([float(i/scalers[2]) for i in dZ])
        )
    (xRan, yRan, zRan) = (aux.axisRange(i) for i in (xN, yN, zN))
    (xi, yi) = (
            np.linspace(xRan[0], xRan[1], NDX),
            np.linspace(yRan[0], yRan[1], NDY)
        )
    zi = griddata((xN, yN), zN, (xi[None, :], yi[:, None]), method=mthd)
    # Return variables
    ranges = (xRan, yRan, zRan)
    grid = (xN, yN, zN)
    surf = (xi, yi, zi)
    return {'ranges': ranges, 'grid': grid, 'surface': surf}


###############################################################################
# Filters
###############################################################################
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


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'TRACES/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.bz'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


def getTTX(PT_OUT, relNum, AOI, QNT, TTX, id, thPlt):
    pt = '{}*{}*{}*{}*{}*.csv'
    WOPfls = glob(pt.format(PT_OUT, str(relNum).zfill(2), AOI, QNT, TTX))[0]
    WOPpds = pd.read_csv(WOPfls)
    fltr = filterFromName(WOPpds, id)
    ttx = WOPpds[fltr][thPlt].values[0]
    return ttx


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
    mxDays = len(prb[0])
    for s in range(smpNum):
        # TTI, TTO, WOP -------------------------------------------------------
        refPop = meanRef['population']
        ratioOI = monet.getPopRatio(prb[s], refPop, gIx)
        thsArrayI = monet.comparePopToThresh(ratioOI, thresholds, cmprOp=op.lt)
        thsArrayO = monet.comparePopToThresh(ratioOI, thresholds, cmprOp=op.gt)
        thsDaysI = monet.thresholdMet(thsArrayI)
        thsDaysO = monet.thresholdMet(thsArrayO)
        # wopArr[s] = [len(i) for i in thsDaysI]
        ttiArr[s] = [min(i) for i in thsDaysI]
        ttoTemp = []
        for (j, dayI) in enumerate(ttiArr[s]):
            if np.isnan(dayI):
                ttoTemp.append(np.nan)
            else:
                ix = np.argmax(thsDaysO[j] > dayI)
                if ix > 0:
                    ttoTemp.append(thsDaysO[j][ix])
                else:
                    ttoTemp.append(mxDays)
                # ttoTemp.append(next(val for x, val in enumerate(thsDaysO[j]) if val > dayI))
        ttoArr[s] = ttoTemp
        wopArr[s] = ttoArr[s] - ttiArr[s]
        # print("\nTTO: {}".format(ttoArr[s]))
        # print("TTI: {}".format(ttiArr[s]))
        # print("WOP: {}".format(wopArr[s]))
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
