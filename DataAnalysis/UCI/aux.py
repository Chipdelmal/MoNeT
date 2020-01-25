#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet

# #############################################################################
# Terminal aesthetics
# #############################################################################
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
colors = ['#0038a8', '#ff0098', '#ffffff']  # '#9f00cc']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)

STYLE_HLT = {
        "width": .05, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 3 * 365], "yRange": [0, 525066.0],
        "colors": colors
    }
STYLE_HLT['aspect'] = monet.scaleAspect(.15, STYLE_HLT)
