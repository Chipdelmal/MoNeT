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


(USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, AOI, REL, LND) = ('dsk', 'HLT', 'gravidFemale', 'PAN')
(DRV, FMT, OVW, FZ) = ('LDR', 'bz2', True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
PT_IMG = PT_IMG + 'preTraces/'
monet.makeFolder(PT_IMG)
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
tyTag = ('sum', 'srp')
if FZ:
    fLists = list(zip(*[fun.getFilteredFiles(
            PT_PRE+'*_00_*'+AOI+'*'+tp+'*',
            PT_PRE+'*'+AOI+'*'+tp+'*') for tp in tyTag]
        ))
else:
    fLists = list(zip(
            *[sorted(glob(PT_PRE+'*'+AOI+'*'+tp+'*')) for tp in tyTag]
        ))
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
