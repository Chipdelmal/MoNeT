#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_gene as drv
import tGD_plots as plot
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, DRV, AOI) = ('dsk', 'linkedDrive', 'HLT')
(FMT, SKP, MF, FZ) = ('bz', False, (True, True), True)
(QNT, thPlt) = ('90', '0.5')  # Change this QNT when the new pst are out!!!!!!!
EXP = ('000', '001', '005', '010', '100')
GRP = (0, 1)
###############################################################################
(grp, exp) = (GRP[0], EXP[0])
for grp in GRP:
    for exp in EXP:
        grpPad = str(grp).zfill(11)
        #######################################################################
        # Setting up paths and style
        #######################################################################
        # Paths ---------------------------------------------------------------
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
        aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Traces ' + AOI)
        #######################################################################
        # Load preprocessed files lists
        #######################################################################
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
        #######################################################################
        # Process files
        #######################################################################
        (xpNum, digs) = monet.lenAndDigits(fLists)
        msg = '* Analyzing ({}/{})'
        for i in range(0, xpNum):
            print(
                    msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)),
                    end='\r'
                )
            # Preprocessed data (sum and rep) ---------------------------------
            (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
            name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
            # Thresholds timing data ------------------------------------------
            id = [int(i) for i in name.split('-')[0].split('_')[1:]]
            id.extend([grp])
            relNum = id[4]
            ttx = (
                    fun.getTTX(PT_OUT, relNum, AOI, QNT, 'TTI', id, thPlt),
                    fun.getTTX(PT_OUT, relNum, AOI, QNT, 'TTO', id, thPlt)
                )
            ttx = [sumDta['population'].shape[0] if math.isnan(i) else i for i in ttx]
            ssv = fun.getTTX(PT_OUT, relNum, AOI, QNT, 'TTS', id, 'ssv')
            ssv = 0 if (math.isnan(ssv)) else ssv
            # Export plots ----------------------------------------------------
            plot.exportTracesPlot(
                    repDta, name+'_Q'+QNT, STYLE, PT_IMG,
                    vLines=ttx, hLines=ssv
                )
        cl = [i[:-2]+'cc' for i in CLR]
        monet.exportGeneLegend(
                sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
            )
        tE = datetime.now()
        print('* Analyzed ({}/{})             '.format(xpNum, xpNum), end='\n')
        print(monet.PAD)
