#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet


# #############################################################################
# Style
# #############################################################################
def getStyle(colors, aspect, xRange, yRange):
    style = {
            "width": .1, "alpha": .1, "dpi": 500,
            "legend": True, "aspect": .5,
            "xRange": xRange, "yRange": yRange,
            "colors": colors
        }
    style['aspect'] = monet.scaleAspect(.2, style)
    return style


# #############################################################################
# Paths
# #############################################################################
def selectPath(USR, DRV):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/SvR/sims/{}/'.format(DRV)
    else:
        PATH_ROOT = '/media/chipdelmal/cache/Sims/SvR/sims/{}/'.format(DRV)
    monet.makeFolder('{}out/'.format(PATH_ROOT))
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}out/'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT)
