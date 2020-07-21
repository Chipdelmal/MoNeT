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
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.xaxis.set_tick_params(width=1)
    axTemp.yaxis.set_tick_params(width=1)
    axTemp.xaxis.set_ticks(np.arange(0, 5*365, 365))
    axTemp.yaxis.set_ticks(np.arange(0, 500000, 500000/4))
    axTemp.grid(which='major', axis='y', lw=.75, alpha=0.25, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.75, alpha=0.25, color=(0, 0, 0))
    axTemp.vlines(
            vLines, 0, 1,
            transform=axTemp.get_xaxis_transform(),
            colors='#000000A5',  # '#FF007FA5'
            linestyles='dashed', linewidth=1, zorder=5
        )
    # axTemp.set_xticks(range(0, STYLE["xRange"][1], 150))
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}-{}.png".format(PATH_IMG, nS, append),
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
# Preprocess Data
###############################################################################
def preProcessSubLandscape(
            pop, landReps, fName, drive,
            nodesAggLst, nodeAggIx,
            MF=(True, True), cmpr='bz2',
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True
        ):
    """
    Preprocesses a subset of the landscape
    Args:
        pop (list): Files list element aggregated by landscape subset
        landReps (dict): Landscape repetitions
                (spatial from monet.loadAndAggregateLandscapeDataRepetitions)
        fName (str): Filename (including path)
        drive (dict): Gene-drive dictionary
        nodesAggLst (lst): List of lists containing the indices of the nodes
                to be aggregated together
        nodeAggIx (int): Current list to process (from the nodeAggLst)
        MF (bool tuple): Male and Female boolean selectors
        cmpr (str): Compression algorithm to be used by compress-python
        SUM (bool): Population summed and gene-aggregated into one node
        AGG (bool): Population gene-aggregated in their own nodes
        SPA (bool): Genetic landscape (gene-aggregated)
        REP (bool): Garbage gene-aggregated data
        SRP (bool): Summed into one garbage gene-aggregated data
    Returns:
        None
    """
    if SUM:
        sumData = monet.sumLandscapePopulationsFromFiles(pop, MF[0], MF[1])
        sumAgg = monet.aggregateGenotypesInNode(sumData, drive)
        pkl.dump(sumAgg, fName+'_sum', compression=cmpr)
    if AGG:
        aggData = monet.loadAndAggregateLandscapeData(pop, drive, MF[0], MF[1])
        pkl.dump(aggData, fName+'_agg', compression=cmpr)
    if SPA:
        geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
        pkl.dump(geneSpaTemp, fName+'_spa', compression=cmpr)
    if REP or SRP:
        fLandReps = monet.filterAggregateGarbageByIndex(
                landReps, nodesAggLst[nodeAggIx]
            )
        pkl.dump(fLandReps, fName+'_rep', compression=cmpr)
    if SRP:
        fRepsSum = [sum(i) for i in fLandReps['landscapes']]
        fRepsDict = {
                'genotypes': fLandReps['genotypes'],
                'landscapes': fRepsSum
            }
        pkl.dump(fRepsDict, fName+'_srp', compression=cmpr)
    return None


def preProcessLandscape(
            pathMean, pathTraces, expName, drive, prePath='./',
            nodesAggLst=[[0]], analysisOI='HLT', fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True
        ):
    """
    Preprocesses a subset of the landscape
    Args:
        pathMean (str): Files list element aggregated by landscape subset
        pathTraces (str): Landscape repetitions
                (spatial from monet.loadAndAggregateLandscapeDataRepetitions)
        expName (str): Filename (including path)
        drive (dict): Gene-drive dictionary
        prePath (str): Preprocess path for export
        nodesAggLst (int): Current list to process (from the nodeAggLst)
        analysisOI (str): ID for type of analysis (HLT or ECO for now)
        fNameFmt (str): Format string for the experiments (prePath+expName+AOI)
        MF (bool tuple): Male and Female boolean selectors
        nodeDigits
        cmpr (str): Compression algorithm to be used by compress-python
        SUM (bool): Population summed and gene-aggregated into one node
        AGG (bool): Population gene-aggregated in their own nodes
        SPA (bool): Genetic landscape (gene-aggregated)
        REP (bool): Garbage gene-aggregated data
        SRP (bool): Summed into one garbage gene-aggregated data
    Returns:
        None
    """
    dirsTraces = monet.listDirectoriesWithPathWithinAPath(pathTraces)
    files = monet.readExperimentFilenames(pathMean)
    filesList = [monet.filterFilesByIndex(files, ix) for ix in nodesAggLst]
    landReps = None
    if REP:
        landReps = monet.loadAndAggregateLandscapeDataRepetitions(
                dirsTraces, drive, MF[0], MF[1]
            )
    for (nodeAggIx, pop) in enumerate(filesList):
        fName = fNameFmt + str(nodeAggIx).zfill(nodeDigits)
        preProcessSubLandscape(
                    pop, landReps, fName, drive,
                    nodesAggLst, nodeAggIx,
                    MF=MF, cmpr=cmpr,
                    SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
                )
    return None


def preProcess(
            exIx, expNum, expDirsMean, expDirsTrac,
            drive, analysisOI='HLT', prePath='./',
            nodesAggLst=[[0]], outExpNames={},
            fNameFmt='{}/{}-{}_', OVW=True,
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True
        ):
    """
    Preprocesses a subset of the landscape
    Args:
        exIx (str): Files list element aggregated by landscape subset
        expNum (str):
        expDirsMean (str): Path to the ANALYZED folder
        expDirsTrac (str): Path to the GARBAGE folder
        drive (dict): Gene-drive dictionary
        analysisOI (str): ID for type of analysis (HLT or ECO for now)
        prePath (str): Preprocess path for export
        outExpNames (set): Experiments names already preprocessed
        nodesAggLst (int): Current list to process (from the nodeAggLst)
        fNameFmt (str): Format string for the experiments (prePath+expName+AOI)
        MF (bool tuple): Male and Female boolean selectors
        nodeDigits (int): Number of digits to be used for nodes padding
        OVW (bool): Overwrite existing experiments (in outExpNames)
        cmpr (str): Compression algorithm to be used by compress-python
        SUM (bool): Population summed and gene-aggregated into one node
        AGG (bool): Population gene-aggregated in their own nodes
        SPA (bool): Genetic landscape (gene-aggregated)
        REP (bool): Garbage gene-aggregated data
        SRP (bool): Summed into one garbage gene-aggregated data
    Returns:
        None
    """
    # Setup paths -------------------------------------------------------------
    strInt = str(exIx+1).zfill(len(str(expNum)))
    print('* Analyzing ({}/{})'.format(strInt, str(expNum)), end='\r')
    (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx]+'/')
    expName = pathMean.split('/')[-1]
    if not((expName in outExpNames) and (OVW)):
        fNameFmt = '{}/{}-{}_'.format(prePath, expName, analysisOI)
        preProcessLandscape(
                    pathMean, pathTraces, expName, drive, prePath,
                    analysisOI=analysisOI, nodesAggLst=nodesAggLst,
                    fNameFmt=fNameFmt, MF=MF, cmpr=cmpr, nodeDigits=nodeDigits,
                    SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
                )
    return None


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
