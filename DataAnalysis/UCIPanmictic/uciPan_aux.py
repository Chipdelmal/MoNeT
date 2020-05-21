#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet


XP_NPAT = 'E_{}_{}_{}_{}-{}_{}_{}.lzma'


def selectPath(USR, LAND, SET, DRIVE_ID):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/{}/'.format(LAND, SET)
    else:
        PATH_ROOT = '/media/chipdelmal/cache/Sims/Panmictic/{}/{}/'.format(
                LAND, SET
            )
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT)


# #############################################################################
# Terminal aesthetics
# #############################################################################
CSV_PAD = 5 * 365
PAD = '' + 75 * '*' + ''
PADL = '' + 75 * '-' + ''
(CRED, CYEL, CBMA, CBRE, CBBL, CWHT, CEND) = (
        '\033[91m', '\u001b[33m', '\u001b[35;1m',
        '\u001b[31;1m', '\u001b[34;1m', '\u001b[37m',
        '\033[0m'
    )

# #############################################################################
# Colors
# #############################################################################
# Health ----------------------------------------------------------------------
colorsH = ['#0000ff20', '#ff000020', '#ffffff00']  # '#9f00cc']
cmapsH = monet.generateAlphaColorMapFromColorArray(colorsH)

STYLE_HLT = {
        "width": .2, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 1825], "yRange": [0, 10100],  # [0, 525066.0],
        "colors": colorsH
    }
STYLE_HLT['aspect'] = monet.scaleAspect(.3, STYLE_HLT)

# Ecology ---------------------------------------------------------------------
colorsE = [
        '#ff004d', '#80ff80', '#6600ff',
        '#e600ff', '#b3ccff', '#333380', '#f0a6ca'
    ]
STYLE_ECO = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 2000], "yRange": [0, 1],
        "colors": colorsE
    }
STYLE_ECO['aspect'] = monet.scaleAspect(.25, STYLE_ECO)
cmapsE = monet.generateAlphaColorMapFromColorArray(colorsE)
