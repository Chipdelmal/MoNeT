#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = ('dsk', 'replacement', sys.argv[1])
(FMT, SKP, MF) = ('bz', False, (True, True))
(QNT, THR, GRP) = ('95', [.05, .10, .25, .50, .75], 0)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
thPlt = [.05, .5]
###############################################################################
# Setting up paths and style
###############################################################################
PST_TYP = ('WOP', 'TTI', 'TTO')
header = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group']
header.extend(THR)
ptrn = '{}*{}*{}.csv'
# Paths -----------------------------------------------------------------------
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
if (AOI == 'ECO'):
    (CLR, CMAPS, YRAN) = (drv.COLEN, drv.COLEM, [0, 200 * 12000])
else:
    (CLR, CMAPS, YRAN) = (drv.COLHN, drv.COLHM, [0, 100 * 12000])
STYLE = {
        "width": .5, "alpha": .15, "dpi": 2*300, "legend": True,
        "aspect": .25, "colors": CLR,
        "xRange": [0, 365 * 3], "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Traces')
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'rep')
fLists = list(zip(*[sorted(glob(PT_PRE+'*'+AOI+'*'+tp+'*')) for tp in tyTag]))
fLists.reverse()
###############################################################################
# Process files
###############################################################################
(xpNum, digs) = monet.lenAndDigits(fLists)
msg = '* Analyzing ({}/{})'
for i in range(0, xpNum):
    print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
    # Preprocessed data (sum and rep) -----------------------------------------
    (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
    # Thresholds timing data --------------------------------------------------
    id = [int(i) for i in name.split('-')[0].split('_')[1:]]
    id.extend([GRP])
    WOPfls = [glob(ptrn.format(PT_OUT, QNT, i))[0] for i in PST_TYP]
    WOPpds = [pd.read_csv(i, names=header) for i in WOPfls]
    fltr = fun.filterFromName(WOPpds[0], id, header)
    WOPval = [list(df[fltr][thPlt].values[0]) for df in WOPpds]
    # Export plots ------------------------------------------------------------
    fun.exportTracesPlot(
            repDta, name, STYLE, PT_IMG, append='TRA',
            vLines=fun.flatten(WOPval[1:])
        )
    cl = [i[:-2]+'cc' for i in CLR]
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
    )
tE = datetime.now()
print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
print(monet.PAD)
