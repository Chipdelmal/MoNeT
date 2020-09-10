#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import matplotlib
import numpy as np
# import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet


XP_NPAT = 'E_{}_{}_{}_{}_{}-{}_{}_{}.{}'


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


# #############################################################################
# Paths
# #############################################################################
def selectPath(USR, LND, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/STP/{}/sim/{}/'.format(LND, EXP)
    else:
        PATH_ROOT = '/media/chipdelmal/cache/Sims/STP/sim/{}/{}/'.format(LND, EXP)
        # PATH_ROOT = '/media/chipdelmal/cache/Sims/SvR/simAlt/{}/'.format(DRV)
    # monet.makeFolder('{}/'.format(PATH_ROOT))
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT)


# #############################################################################
# Color Palette
# #############################################################################
[i/255 for i in (70, 80, 255)]
cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)),
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
