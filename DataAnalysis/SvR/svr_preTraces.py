#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = (sys.argv[1], 'replacement', sys.argv[2])
(FMT, SKP, MF) = ('bz2', False, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
if (AOI == 'ECO'):
    (CLR, CMAPS, YRAN) = (drv.COLEN, drv.COLEM, [0, 200 * 12000])
else:
    (CLR, CMAPS, YRAN) = (drv.COLHN, drv.COLHM, [0, 100 * 12000])
STYLE = {
        "width": .5, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .25,
        "colors": CLR, "xRange": [0, 365 * 3], "yRange": YRAN
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
    (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
    # Export plots ------------------------------------------------------------
    fun.exportTracesPlot(repDta, name, STYLE, PT_IMG, append='TRA')
    cl = [i[:-2]+'cc' for i in CLR]
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
    )
tE = datetime.now()
print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
print(monet.PAD)
