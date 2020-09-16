#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
# import os as os
# import csv as csv
import matplotlib
import pandas as pd
# import numpy as np
import MoNeT_MGDrivE as monet


XP_NPAT = 'E_{}_{}_{}_{}_{}_{}-{}_{}_{}.bz'


# #############################################################################
# Count genotypes
# #############################################################################
def countGeneAppearances(genotypes, gene, pos):
    # Split genotypes
    splitGenotypes = [list(genes) for genes in genotypes]
    # Count
    appearances = []
    for p in pos:
        slot = [gene[p] for gene in splitGenotypes]
        matches = re.finditer(gene, ''.join(slot))
        appearances.extend([match.start() for match in matches])
    appearances.sort()
    return appearances


def flatten(l): return [item for sublist in l for item in sublist]


def aggregateGeneAppearances(genotypes, genes):
    gcnt = [countGeneAppearances(genotypes, gn[0], gn[1]) for gn in genes]
    return sorted(flatten(gcnt))


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, DRV, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/tGD/figure2/{}/{}/'.format(DRV, EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/media/hdd/WorkExperiments/tGD/figure2/{}/{}/'.format(DRV, EXP)
    elif USR == 'PZ':
        PATH_ROOT = '/PATH_TO_FOLDER/tGD/figure2/{}/{}/'.format(DRV, EXP)
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/tGD/figure2/{}/{}/'.format(DRV, EXP)
    # monet.makeFolder('{}/'.format(PATH_ROOT))
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT)


def selectDepVars(MOI, AOI):
    # Select ranges and dependent variable
    if (MOI == 'WOP') or (MOI == 'TTI') or (MOI == 'TTO'):
        scalers = (1, 100, round(2.5*365))
        (HD_DEP, IND_RAN) = ('0.1', 7)
    else:
        scalers = (1, 100, 5000)
        (HD_DEP, IND_RAN) = ('ssv', 7)
    # Color Mapping
    if AOI == 'HLT':
        cmap = cmapB
    else:
        cmap = cmapM
    return (scalers, HD_DEP, IND_RAN, cmap)


def setupFolder(USR, DRV, exp, HD_IND):
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = selectPath(USR, DRV, exp)
    PT_IMG = PT_IMG[:-1]+'Pst/'
    fldrName = '{}_{}/'.format(*HD_IND)
    PT_IMG_XP = PT_IMG+fldrName
    monet.makeFolder(PT_IMG)
    monet.makeFolder(PT_IMG_XP)
    return (PT_ROT, PT_IMG_XP, PT_DTA, PT_PRE, PT_OUT)


def loadDFFromFiles(fName, IND_RAN):
    df = pd.read_csv(fName[0])
    for filename in fName:
        df = df.append(pd.read_csv(filename))
    header = list(df.columns)
    headerInd = header[:IND_RAN]
    return (df, header, headerInd)


# #############################################################################
# Style
# #############################################################################
def getStyle(colors, aspectR, xRange, yRange):
    style = {
            "width": .1, "alpha": .1, "dpi": 500,
            "legend": True, "aspect": .5,
            "xRange": xRange, "yRange": yRange,
            "colors": colors
        }
    style['aspect'] = monet.scaleAspect(aspectR, style)
    return style


def axisRange(x):
    return (min(x), max(x))


# #############################################################################
# Terminal
# #############################################################################

def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, title):
    print(monet.PAD)
    (cred, cwht, cend) = (monet.CRED, monet.CWHT, monet.CEND)
    print(cwht+'MoNeT '+title+' ['+str(time)+']'+cend)
    print(monet.PAD)
    print('{}* Root: {}{}'.format(cred, PATH_ROOT, cend))
    print('{}* Imgs: {}{}'.format(cred, PATH_IMG, cend))
    print('{}* Data: {}{}'.format(cred, PATH_DATA, cend))
    print(monet.PAD)


# #############################################################################
# Color Palette
# #############################################################################
[i/255 for i in (70, 80, 255)]
cdict = {
        'red':  ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.3, 0.3), (1.0, 0.0, 0.0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 0.25, 0.25))
    }
cmapB = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.0, 0.0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.3, 0.3)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 1.0, 1.0))
    }
cmapC = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 1.0, 1.0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.0, 0.0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.3, 0.3))
    }
cmapM = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)
