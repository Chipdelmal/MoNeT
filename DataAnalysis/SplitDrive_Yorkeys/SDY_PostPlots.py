#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import SDY_aux as aux
import SDY_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

(USR, SET) = ('srv', sys.argv[1])  # 'Aggregated')
(TRA, HEA, EXT) = (True, True, '.lzma')
###############################################################################
# Setup paths
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH = '/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/'
else:
    PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
pathPre = '{}pre/{}/'.format(PATH, SET)
pathImg = '{}img/{}/'.format(PATH, SET)
monet.makeFolder(pathImg)
# Colors
(CLR, CMAPS) = (aux.COLORS, aux.CMAPS)
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300, "legend": True,
        "aspect": .5, "colors": CLR, "xRange": [0, 1825], "yRange": [0, 150000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
tSrt = datetime.now()
aux.printExperimentHead(PATH, pathImg, pathPre, str(tSrt), 'Plotting ')
###############################################################################
# List preprocessed files lists
###############################################################################
typTag = ('sum', 'spa', 'rep')  # 'srp')
# typTag = ('sum', 'rep')
fLists = list(zip(*[sorted(glob(pathPre+'*'+tp+EXT)) for tp in typTag]))
###############################################################################
# Load preprocessed files lists
###############################################################################
(xpNum, digs) = fun.lenAndDigits(fLists)
msg = '* Analyzing ({}/{})'
for i in range(0, xpNum):
    print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
    (sumDta, spaDta, repDta, srpDta) = [pkl.load(file) for file in (fLists[i])]
    # (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[-2][:-4]
    # Process data ------------------------------------------------------------
    spaDtaNorm = monet.rescaleGeneSpatiotemporals(spaDta)
    overlay = monet.plotGenotypeOverlayFromLandscape(
            spaDtaNorm, vmax=1,
            style={"aspect": 50 * STYLE['aspect'], "cmap": CMAPS},
         )
    # Export plots ------------------------------------------------------------
    fun.exportTracesPlot(repDta, name, STYLE, pathImg, append='TRA')
    monet.quickSaveFigure(
            overlay,
            '{}/{}-{}.pdf'.format(pathImg, name, 'OVR'), format='pdf'
         )
    monet.exportGeneLegend(sumDta['genotypes'], CLR, pathImg+'/plt.pdf', 500)
tEnd = datetime.now()
print('* Analyzed ({}/{})     '.format(xpNum, xpNum), end='\n')
aux.printExperimentTail(str(tEnd-tSrt), 'Plotting')
