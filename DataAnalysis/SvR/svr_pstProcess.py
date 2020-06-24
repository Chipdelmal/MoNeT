#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
# import compress_pickle as pkl


(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz2', False, (True, True), [.5, .95], True)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
(CLR, CMAPS) = (drv.COLHN, drv.COLHM)
STYLE = {
        "width": .05, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .5,
        "colors": CLR, "xRange": [0, 15*365], "yRange": [0, 100 * 12500]
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Traces')
###############################################################################
# Quantiles calculation for experiments
###############################################################################
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(rrt, rnm, fit, svr, gne, grp) = uids[1:]
# Base experiments
bsPat = aux.XP_NPAT.format('*', '00', '*', '*', AOI, '*', 'sum*')
bsFiles = sorted(glob(PT_PRE+bsPat))
existing = glob(PT_OUT+'*')
