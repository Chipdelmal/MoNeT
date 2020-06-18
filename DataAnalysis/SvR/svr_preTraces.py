#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(FMT, SKP, MF) = ('bz2', False, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
(CLR, CMAPS) = (drv.COLHN, drv.COLHM)
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .5,
        "colors": CLR, "xRange": [0, 1825], "yRange": [0, 100 * 12500]
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Traces')
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'rep')
fLists = list(zip(*[sorted(glob(PT_PRE+'*'+tp+'*')) for tp in tyTag]))
fLists.reverse()
###############################################################################
# Process files
###############################################################################
(xpNum, digs) = monet.lenAndDigits(fLists)
msg = '* Analyzing ({}/{})'
for i in range(0, xpNum):
    print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
    (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[-3][:-4]
    # Export plots ------------------------------------------------------------
    fun.exportTracesPlot(repDta, name, STYLE, PT_IMG, append='TRA')
    cl = [i[:-2]+'cc' for i in CLR]
    monet.exportGeneLegend(sumDta['genotypes'], cl, PT_IMG+'/plt.png', 500)
tE = datetime.now()
print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
print(monet.PAD)
