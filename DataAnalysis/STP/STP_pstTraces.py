#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_functions as fun
import STP_dataProcess as da
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


# (USR, DRV, AOI, REL, LND) = (sys.argv[1], 'LDR', sys.argv[2], sys.argv[3], sys.argv[4])
(USR, DRV, AOI, REL, LND) = ('dsk', 'LDR', 'HLT', 'mixed', 'PAN')
(SKP, THS, QNT, OVW, FZ) = (False, '0.1', '90', True, True)

(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
PT_IMG = PT_IMG + 'pstTraces/'
monet.makeFolder(PT_IMG)
drive = drv.driveSelector(DRV)
gene = drive.get(AOI).get('gDict')
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
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
aux.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PstTraces')
