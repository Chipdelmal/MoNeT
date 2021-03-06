#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import csv
import numpy as np
import pandas as pd
import operator as op
from glob import glob
import uciPan_aux as aux
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt


def loadDataset(expSet, fileCode, fileBool):
    dta = None
    fltr = list(filter(lambda x: fileCode in x, expSet))
    if (len(fltr) > 0) and (fileBool):
        dta = pkl.load(fltr[0], compression="lzma")
    return dta


def splitExpNames(PATH_OUT):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.lzma')]
    return sorted(list(set(out)))


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.lzma'):
    filesList = glob(PATH_EXP+'*'+ext)
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


###############################################################################
# Pops Thresholds
###############################################################################
def comparePopToThresholds(ratioOI, thresholds, cmprOp=op.lt):
    flagsArray = np.empty((len(ratioOI), len(thresholds)), dtype=bool)
    for (i, dayData) in enumerate(ratioOI):
        closeFlags = [cmprOp(dayData, i) for i in thresholds]
        flagsArray[i] = closeFlags
    return flagsArray


def getPopRatio(prbPop, refPop, gIx):
    (a, b) = (prbPop, refPop)
    ratio = np.divide(a, b, out=np.zeros_like(a), where=b != 0)
    ratioOI = [row[gIx] for row in ratio]
    return ratioOI


def trueIndices(boolList):
    trueIx = [i for (i, x) in enumerate(boolList) if x == 1]
    if len(trueIx) > 0:
        return trueIx
    else:
        return [np.nan]


def thresholdMet(thsArray):
    thsNum = len(thsArray[0])
    thrsMet = [None] * thsNum
    for col in range(thsNum):
        boolCol = [i[col] for i in thsArray]
        daysAbove = trueIndices(boolCol)
        thrsMet[col] = daysAbove
    return thrsMet


def calcMeanTTI(meanPrb, meanRef, thresholds, gIx):
    ratioOI = getPopRatio(meanPrb['population'], meanRef['population'], gIx)
    thsArray = comparePopToThresholds(ratioOI, thresholds)
    thsDays = thresholdMet(thsArray)
    ttiAn = [i[0] for i in thsDays]
    return ttiAn


def calcQuantTTI(srpPrb, meanRef, thresholds, gIx, quantile=.95):
    prb = srpPrb['landscapes']
    smpNum = len(prb)
    ttiArr = np.empty((smpNum, len(thresholds)))
    for s in range(smpNum):
        refPop = meanRef['population']
        ratioOI = getPopRatio(prb[s], refPop, gIx)
        thsArray = comparePopToThresholds(ratioOI, thresholds)
        thsDays = thresholdMet(thsArray)
        ttiArr[s] = [i[0] for i in thsDays]
    quant = np.nanquantile(ttiArr, quantile, axis=0)
    return quant


def calcMeanWOP(meanPrb, meanRef, thresholds, gIx):
    ratioOI = getPopRatio(meanPrb['population'], meanRef['population'], gIx)
    thsArray = comparePopToThresholds(ratioOI, thresholds)
    thsDays = thresholdMet(thsArray)
    ttiAn = [len(i) for i in thsDays]
    return ttiAn


def calcQuantWOP(srpPrb, meanRef, thresholds, gIx, quantile=.95):
    prb = srpPrb['landscapes']
    smpNum = len(prb)
    ttiArr = np.empty((smpNum, len(thresholds)))
    for s in range(smpNum):
        refPop = meanRef['population']
        ratioOI = getPopRatio(prb[s], refPop, gIx)
        thsArray = comparePopToThresholds(ratioOI, thresholds)
        thsDays = thresholdMet(thsArray)
        ttiArr[s] = [len(i) for i in thsDays]
    quant = np.nanquantile(ttiArr, quantile, axis=0)
    return quant


###############################################################################
# Dynamics
###############################################################################
# def filterFilesByIndex(files, ix, male=True, female=True):
#     m = [files['male'][z] for z in ix] if male else []
#     f = [files['female'][z] for z in ix] if female else []
#     ffiles = {'male': m, 'female': f}
#     return ffiles
#
#
# def filterGarbageByIndex(landRepetition, indices):
#     return list(map(landRepetition.__getitem__, indices))
#
#
# def filterAggregateGarbageByIndex(landscapeReps, indices):
#     genes = landscapeReps['genotypes']
#     repsNumber = len(landscapeReps['landscapes'])
#     traces = []
#     for j in range(0, repsNumber):
#         probe = landscapeReps['landscapes'][j]
#         trace = np.sum(filterGarbageByIndex(probe, indices), axis=0)
#         traces.append([trace])
#     filteredLand = {'genotypes': genes, 'landscapes': traces}
#     return filteredLand

def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append=''):
    figArr = monet.plotLandscapeDataRepetitions(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
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


###############################################################################
# Main Spatial
###############################################################################
def printExpTerminal(time, PATH_ROOT, PATH_IMG, PATH_DATA):
    print(aux.PAD)
    printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, str(time))
    expOutRootPath = PATH_IMG
    monet.makeFolder(expOutRootPath)


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'GARBAGE/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


###############################################################################
# Experiment Selection and Terminal
###############################################################################
def importThresholdsCSV(path, names):
    fxLst = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            xpID = row[0].split('_')[1:]
            xpDT = row[1:]
            xpID.extend(xpDT)
            fxLst.append(xpID)
    return pd.DataFrame(fxLst, columns=names)


def ammendHeader(xpNames, thsID):
    thsID = ['W'+i for i in thsID]
    thsID.reverse()
    xpNames.extend(thsID)
    return xpNames


###############################################################################
# Crosses and timing
###############################################################################
def getSSPopsInLandscape(aggregatedNodesData, ssDay):
    ssPops = []
    for node in aggregatedNodesData['landscape']:
        ssPops.append(node[ssDay - 1][-1])
    return ssPops


def getTracesAndMeanDirs(pathTraces, pathMean):
    (dirsTraces, dirsMean) = (
            monet.listDirectoriesWithPathWithinAPath(pathTraces),
            monet.listDirectoriesWithPathWithinAPath(pathMean)
        )
    return (dirsTraces, dirsMean)


def calcDaysCrosses(aggregatedNodesData, thresholds, ssPops, gIx):
    chngDays = []
    for j in range(len(aggregatedNodesData['landscape'])):
        nodePop = aggregatedNodesData['landscape'][j]
        thrsBool = monet.comparePopToThresholds(
                nodePop, gIx, [0, 1], thresholds, refPop=ssPops[j]
            )
        chngDays.append(monet.getConditionChangeDays(thrsBool))
    return chngDays


def getTimeToMinAtAllele(aggData, gIx, safety=.1):
    pop = [row[gIx] for row in aggData['population']]
    for time in range(len(pop)):
        popMin = min(pop)
        if np.isclose(pop[time], popMin, atol=safety):
            break
    return (time, popMin)


def padListLength(inList, length, pad=0):
    inList += [pad] * (length - len(inList))
    return inList


###############################################################################
# Experiment Selection and Terminal
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


def experimentSelector(args):
    # Device
    if args.dev == 0:
        ROOT = '/Volumes'
    else:
        ROOT = '/RAID5'
    # Landscape
    if args.land == 0:
        LAND = 'Comoros'
    else:
        LAND = 'STP'
    # Selected IDs
    return (ROOT, LAND)


def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time):
    print(
            aux.CWHT + 'UCI Experiments Analysis '
            + '[' + time + ']' + aux.CEND
        )
    print(aux.PADL)
    print(aux.CRED + '* Root  PATH: ' + PATH_ROOT + aux.CEND)
    print(aux.CRED + '* Data  PATH: ' + PATH_DATA + aux.CEND)
    print(aux.CRED + '* Image PATH: ' + PATH_IMG + aux.CEND)


###############################################################################
# Experiment Selection and Terminal
###############################################################################
def listDirectoriesWithPathWithinAPath(pathFilename):
    '''
    Description:
        * Returns a list of folder paths within a given path.
    In:
        * pathFilename: Path to search directories in
    Out:
        * List of folder paths
    Notes:
        * NA
    '''
    folders = monet.listDirectoriesInPath(pathFilename)
    for i, folder in enumerate(folders):
        folders[i] = pathFilename + '/' + folder
    return folders


###############################################################################
# Style and colors
###############################################################################
def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


def lenAndDigits(collection):
    """Returns the length of a list and the number of digits for z-padding
    Args:
        collection (list): Collection of elements with the "len" method
            implemented.
    Returns:
        tuple: (number of elements in the collection, required digits)
    """
    length = len(collection)
    digs = len(str(length))
    return (length, digs)
