#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from glob import glob
import pandas as pd
import SDY_aux as aux
import SDY_gene as drv
import SDY_plot as plt
import SDY_expWrangler as exp
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


# (USR, AOI, THS, QNT) = (sys.argv[1], sys.argv[2], 0.2, '90')
(USR, AOI, THS, QNT) = ('dsk', 'HLT', 0.5, '90')
(DRV, EXP) = ('SD', 'factorial')
(OVW, JOB, gIx, FZ) = (True, 4, 1, False)
# Select surface variables ----------------------------------------------------
HD_IND = ['i_ren', 'i_hnf']
(ngdx, ngdy) = (1000, 1000)
(lvls, mthd, xSca, ySca) = (
        [-.05, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1],
        'linear', 'linear', 'linear'
    )
MOI = ('TTI', 'TTO', 'WOP', 'MNX', 'RAP')
for moi in MOI:
    (scalers, HD_DEP, _, cmapR) = aux.selectDepVars(moi, AOI)
    cmap = cmapR.reversed()
