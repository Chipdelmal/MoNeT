#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from glob import glob
import pandas as pd
import SDY_aux as aux
import SDY_gene as drv
import SDY_plot as plt
import SDY_expWrangler as exp
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


# (USR, AOI, THS, QNT) = (sys.argv[1], sys.argv[2], 0.50, '90')
(USR, AOI, THS, QNT) = ('dsk', 'HLT', 0.5, '50')
(DRV, EXP) = ('SD', 'factorial')
(OVW, JOB, gIx, FZ) = (True, 4, 1, False)
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
PT_IMG = PT_IMG + 'pstTraces/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
drive = drv.driveSelector(DRV, AOI)
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .25, "alpha": .15, "dpi": 250, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*5)/3],
        "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PstTraces')
###########################################################################
# Load postprocessed files
###########################################################################
pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
pstFiles = [pstPat.format(i) for i in ('TTI', 'TTO', 'WOP', 'MNX', 'RAP')]
(dfTTI, dfTTO, dfWOP, dfMNX, _) = [pd.read_csv(i) for i in pstFiles]
###############################################################################
# Load preprocessed files lists
###############################################################################
repFiles = glob(PT_PRE+'*'+AOI+'*'+'srp'+'*')
if FZ:
    fLists = aux.getFilteredFiles(
        PT_PRE+'*_00_*'+AOI+'*srp.bz',
        PT_PRE+'*'+AOI+'*'+'*srp.bz'
    )
else:
    fLists = glob(PT_PRE+'*'+AOI+'*'+'*srp.bz')
###########################################################################
# Iterate through experiments
###########################################################################
msg = '* Plotting ({}/{})'
filesNum = len(repFiles)
for (i, repFile) in enumerate(repFiles):
    print(msg.format(i+1, filesNum), end='\r')
    (repDta, xpid) = (
            pkl.load(repFile),
            exp.getXpId(repFile, [1, 2, 3, 4, 5, 7])
        )
    xpRow = [monet.filterDFWithID(i, xpid) for i in (dfTTI, dfTTO, dfWOP, dfMNX)]
    (tti, tto, wop) = [float(row[str(THS)]) for row in xpRow[:3]]
    (mnf, mnd) = (float(xpRow[3]['min']), float(xpRow[3]['minx']))
    pop = repDta['landscapes'][0][0][-1]
    plt.exportTracesPlot(
            repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
            vLines=[tti, tto, mnd], hLines=[mnf*pop]
        )
monet.exportGeneLegend(
        repDta['genotypes'], [i[:-2]+'cc' for i in CLR],
        PT_IMG+'/plt_{}.png'.format(AOI), 500
    )
print(msg.format(i+1, filesNum), end='\r')
