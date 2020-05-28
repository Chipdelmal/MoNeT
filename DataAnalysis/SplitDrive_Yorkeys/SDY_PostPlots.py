#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import SDY_aux as aux
import SDY_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(SET, TRA, HEA, EXT) = ('Aggregated', True, True, '.lzma')
PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
pathPre = '{}pre/{}/'.format(PATH, SET)
pathImg = '{}img/{}/'.format(PATH, SET)
monet.makeFolder(pathImg)
###############################################################################
# Setup paths
###############################################################################
(CLR, CMAPS) = (aux.COLORS, aux.CMAPS)
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300, "legend": True,
        "aspect": .5, "colors": CLR, "xRange": [0, 1825], "yRange": [0, 150000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
tSrt = datetime.now()
aux.printExperimentHead(PATH, pathImg, pathPre, str(tSrt), 'Plotting ')
###############################################################################
# Load preprocessed files lists
###############################################################################
typTag = ('sum', 'spa', 'rep')
fLists = list(zip(*[sorted(glob(pathPre+'*'+tp+EXT)) for tp in typTag]))
###############################################################################
# Load preprocessed files lists
###############################################################################
(xpNum, digs) = monet.lenAndDigits(fLists)
for i in range(0, xpNum):
    print('* Analyzing ({}/{})'.format(str(i).zfill(digs), xpNum), end='\r')
    (sumDta, spaDta, repDta) = [pkl.load(file) for file in (fLists[i])]
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
aux.printExperimentTail(str(tEnd-tSrt), 'Plotting')
