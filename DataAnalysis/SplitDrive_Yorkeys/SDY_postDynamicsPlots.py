#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import numpy as np
import SDY_ix as ix
from glob import glob
import SDY_aux as aux
import SDY_functions as fun
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(SET, TRA, HEA, EXT) = ('Aggregated', True, True, '.lzma')
PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
pathPre = '{}pre/{}/'.format(PATH, SET)
###############################################################################
# Setup paths
###############################################################################
(CLR, CMAPS) = (aux.COLORS, aux.CMAPS)
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300, "legend": True,
        "aspect": .5, "colors": CLR, "xRange": [0, 1825], "yRange": [0, 150000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
###############################################################################
# Load preprocessed files lists
###############################################################################
typTag = ('sum', 'spa')
fLists = list(zip(*[sorted(glob(pathPre+'*'+tp+EXT)) for tp in typTag]))
###############################################################################
# Load preprocessed files lists
###############################################################################
i = 0
(sumDta, spaDta) = [pkl.load(file) for file in (fLists[i])]
