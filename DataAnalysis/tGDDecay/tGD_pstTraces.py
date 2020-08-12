#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from glob import glob
import tGD_aux as aux
import tGD_gene as drv
import tGD_fun as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('dsk', 'linkedDrive', 'HLT')
(FMT, SKP, MF, FZ) = ('bz', False, (True, True), True)
(QNT, THR, GRP) = ('10', [.05, .10, .25, .50, .75], 0)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
thPlt = ['0.5']
EXP = ('000', '001', '005', '010', '100')
# THESE TWO WILL NEED FIX IN THE NEXT VERSION
exp = EXP[1]
grpPad = str(GRP).zfill(11)
###############################################################################
# Setting up paths and style
###############################################################################
PST_TYP = ('WOP', 'TTI', 'TTO')
ptrn = '{}*{}*{}*{}*.csv'
# Paths -----------------------------------------------------------------------
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
PT_IMG = PT_IMG[:-1] + 'Pst/'
monet.makeFolder(PT_IMG)
drive = drv.driveSelector(DRV, AOI)
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .5, "alpha": .15, "dpi": 1*200, "legend": False,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*5)/2],
        "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Traces ' + AOI)
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'rep')
if FZ:
    fLists = list(zip(*[fun.getFilteredFiles(
            PT_PRE+'*_00_*'+AOI+'*'+grpPad+'*'+tp+'*',
            PT_PRE+'*'+AOI+'*'+grpPad+'*'+tp+'*') for tp in tyTag]
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
for i in range(0, xpNum):
    print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
    # Preprocessed data (sum and rep) -----------------------------------------
    (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
    # Thresholds timing data --------------------------------------------------
    id = [int(i) for i in name.split('-')[0].split('_')[1:]]
    id.extend([GRP])
    relNum = id[4]
    WOPfls = [glob(ptrn.format(PT_OUT, relNum, QNT, z))[0] for z in PST_TYP]
    WOPpds = [pd.read_csv(z) for z in WOPfls]
    fltr = fun.filterFromName(WOPpds[0], id)
    WOPval = [len(df[fltr][thPlt].values) for df in WOPpds]
    bools = ([i > 0 for i in WOPval])
    if all(bools):
        WOPval = [list(df[fltr][thPlt].values[0]) for df in WOPpds]
    else:
        WOPval = [[0], [0], [0]]
    # Export plots ------------------------------------------------------------
    fun.exportTracesPlot(
            repDta, name+'_Q'+QNT, STYLE, PT_IMG,
            vLines=fun.flatten(WOPval[1:])
        )
cl = [i[:-2]+'cc' for i in CLR]
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
    )
tE = datetime.now()
print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
print(monet.PAD)
