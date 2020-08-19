#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
from joblib import Parallel, delayed

sys.path.append('C:/Users/prisc/Documents/GitHub/MoNeT2/DataAnalysis/tGDDecay/')
import tGD_aux as aux
import tGD_gene as drv
import tGD_fun as fun

(USR, DRV, AOI) = ('Priscilla', 'tGD', 'HLT')

# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, DRV, AOI) = ('dsk', 'linkedDrive', 'ECO')

(FMT, SKP, MF, FZ) = ('bz2', False, (True, True), True)
EXP = ['000','001']



###############################################################################
# Setting up paths and style
###############################################################################
for exp in EXP:

    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
    drive = drv.driveSelector(DRV, AOI)
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .5, "alpha": .15, "dpi": 1*200, "legend": True,
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

    print('this is pt_pre:',PT_PRE + '*_00_*'+AOI+'*')


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

    sumDta = {}

    def HelperFunction(i):
        print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
        (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
        name = fLists[i][0].split('/')[-1].split('.')[0][:-4][11:]
        # Export plots --------------------------------------------------------
        fun.exportTracesPlot(repDta, name, STYLE, PT_IMG, append='TRA')
        cl = [i[:-2]+'cc' for i in CLR]
        if i == xpNum - 1:
            monet.exportGeneLegend(
                sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
                )
            tE = datetime.now()
            print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
            print(monet.PAD)


    Parallel(n_jobs=4)(delayed(HelperFunction)(i) for i in range(0, xpNum))
