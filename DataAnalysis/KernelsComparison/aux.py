#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet

CSV_PAD = 5 * 365
# #############################################################################
# Terminal aesthetics
# #############################################################################
PAD = '' + 79 * '*' + ''
PADL = '' + 79 * '-' + ''
(CRED, CYEL, CBMA, CBRE, CBBL, CWHT, CEND) = (
        '\033[91m', '\u001b[33m', '\u001b[35;1m',
        '\u001b[31;1m', '\u001b[34;1m', '\u001b[37m',
        '\033[0m'
    )

# #############################################################################
# Colors
# #############################################################################
# Health ----------------------------------------------------------------------
colors = [(0, .22, .66, .1), (1, 0, .6, .1), (1, 1, 1, 0)]
cmapsH = monet.generateAlphaColorMapFromColorArray(colors)
STYLE_HLT = {
        "width": .175, "alpha": .175, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 1095], "yRange": [0, 525066.0],
        "colors": colors
    }
STYLE_HLT['aspect'] = monet.scaleAspect(.15, STYLE_HLT)

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
