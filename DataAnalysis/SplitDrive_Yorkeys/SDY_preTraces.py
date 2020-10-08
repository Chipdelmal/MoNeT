#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import SDY_aux as aux
# import SDY_fun as fun
import SDY_gene as drv
# import tGD_plots as plots
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


# (USR, AOI) = (sys.argv[1], sys.argv[1])
(USR, AOI) = ('dsk', 'HLT')
(DRV, EXP) = ('SD', 'factorial')
(OVW, FZ, JOB) = (True, False, 1)
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
PT_IMG = PT_IMG + 'preTraces/'
monet.makeFolder(PT_IMG)
drive = drv.driveSelector(DRV, AOI)
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .25, "alpha": .15, "dpi": 250, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*6)/3],
        "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'SDY PreTraces')
# #############################################################################
# Process files
# #############################################################################
fLists = aux.getZeroFilteredFiles(PT_PRE, AOI, FZ=FZ, tyTag=('sum', 'srp'))
(xpNum, digs) = monet.lenAndDigits(fLists)
msg = '* Analyzing ({}/{})'
