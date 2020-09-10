#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


# (USR, DRV, AOI, REL, LND) = (sys.argv[1], 'LDR', sys.argv[2], sys.argv[3], sys.argv[4])
(USR, DRV, AOI, REL, LND) = ('dsk', 'LDR', 'HLT', 'mixed', 'PAN')
(FMT, OVW, MF, JOB) = ('bz2', True, (False, True), 2)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, LND, REL)
if (AOI == 'ECO'):
    (CLR, CMAPS, YRAN) = (drv.COLEN, drv.COLEM, [0, 200 * 12000])
else:
    (CLR, CMAPS, YRAN) = (drv.COLHN, drv.COLHM, [0, 100 * 12000 / 2])
STYLE = {
        "width": .5, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .25,
        "colors": CLR, "xRange": [0, 365 * 3], "yRange": YRAN
    }

STYLE['aspect'] = monet.scaleAspect(1, STYLE)
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
i = 0
for i in range(0, xpNum):
    print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
    (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
    # Export plots ------------------------------------------------------------
    fun.exportTracesPlot(repDta, name, STYLE, PT_IMG, append='TRA', vLines=[0, 0])
    cl = [i[:-2]+'cc' for i in CLR]
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
    )
tE = datetime.now()
print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
print(monet.PAD)
