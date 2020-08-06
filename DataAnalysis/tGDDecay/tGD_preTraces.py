#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import tGD_aux as aux
import tGD_gene as drv
import tGD_fun as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, DRV, AOI) = ('dsk', 'linkedDrive', 'ECO')
(FMT, SKP, MF, FZ) = ('bz2', False, (True, True), True)
EXP = ('000', '001', '005', '010', '100')
###############################################################################
# Setting up paths and style
###############################################################################
for exp in EXP:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
    DRV = drv.driveSelector(DRV, AOI)
    (CLR, YRAN) = (DRV.get('colors'), (0, DRV.get('yRange')))
    STYLE = {
            "width": .5, "alpha": .15, "dpi": 2*300, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": [0, (365*5)/2],
            "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    tS = datetime.now()
    fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Traces')
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'rep')
    if FZ:
        fLists = list(zip(*[fun.getFilteredFiles(
                PT_PRE+'*_00_*'+AOI+'*'+tp+'*',
                PT_PRE+'*'+AOI+'*'+tp+'*') for tp in tyTag]
            ))
    else:
        fLists = list(zip(
                *[sorted(glob(PT_PRE+'*'+AOI+'*'+tp+'*')) for tp in tyTag]
            ))
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    msg = '* Analyzing ({}/{})'
    for i in range(0, xpNum):
        print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
        (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
        name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
        # Export plots --------------------------------------------------------
        fun.exportTracesPlot(repDta, name, STYLE, PT_IMG, append='TRA')
        cl = [i[:-2]+'cc' for i in CLR]
    monet.exportGeneLegend(
            sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
        )
    tE = datetime.now()
    print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
    print(monet.PAD)
