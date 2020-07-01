#!/usr/bin/python
# -*- coding: utf-8 -*-

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
def selectPath(USR, DRV):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/SvR/sim/{}/out/LDR/'.format(DRV)
    else:
        PATH_ROOT = '/media/chipdelmal/cache/Sims/SvR/simLocal/{}/out/LDR/'.format(DRV)
    # monet.makeFolder('{}/'.format(PATH_ROOT))
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT)
