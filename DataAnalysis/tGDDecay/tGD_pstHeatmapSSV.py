#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import warnings
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
from itertools import product
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
# ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']


(USR, DRV, AOI, MOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, DRV, AOI, MOI) = ('dsk', 'linkedDrive', 'HLT', 'TTS')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (False, True), [.05, .1, .5], True)
ci = QNT[1]
# Select surface variables ----------------------------------------------------
HD_IND = ['res', 'hnf']
(scalers, HD_DEP, IND_RAN, cmap) = aux.selectDepVars(MOI, AOI)
(ngdx, ngdy) = (1000, 1000)
(lvls, mthd, xSca, ySca) = (
        [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1],
        'linear', 'linear', 'linear'
    )
# Spatial settings to sweep through -------------------------------------------
EXPS = ('000', '001', '005', '010', '100')
###############################################################################
# Loop through the experiments
###############################################################################
for exp in EXPS:
    (PT_ROT, PT_IMG_XP, PT_DTA, PT_PRE, PT_OUT) = aux.setupFolder(
            USR, DRV, exp, HD_IND
        )
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG_XP, PT_PRE, tS, 'Heatmap '+AOI)
    ###########################################################################
    # Analyzes
    ###########################################################################
    # Load files into dataframe
    fPtrn = '{}/*{}*{}-{}.csv'.format(PT_OUT, AOI, str(int(ci*100)), MOI)
    (df, header, headerInd) = aux.loadDFFromFiles(sorted(glob(fPtrn)), IND_RAN)
    # Filter the dataframe ----------------------------------------------------
    # Get the unique values for each indep-var column of the dataframe
    uniqueValues = {i: list(df[i].unique()) for i in headerInd}
    idTuplesAll = list(product(*uniqueValues.values()))
    # Filtering all the experiments of the non-free columns
    hdFree = [col for col in headerInd if col not in HD_IND]
    # Get the unique IDs of the experiments
    uniqueIds = [uniqueValues.get(head) for head in hdFree]
    idTuples = list(product(*uniqueIds))
    # Loop here xpId = idTuples[0]
    xpNum = len(idTuples)
    xpNumS = str(xpNum).zfill(4)
    print(monet.CBBL, end='\r')
    for (xpNumC, xpId) in enumerate(idTuples):
        xpNumCS = str(xpNumC+1).zfill(4)
        print('* Exporting {}/{}'.format(xpNumCS, xpNumS), end='\r')
        #######################################################################
        # Filter
        #######################################################################
        indepFltrs = [list(df[hId[1]] == hId[0]) for hId in zip(xpId, hdFree)]
        fullFilter = list(map(all, zip(*indepFltrs)))
        dfSrf = df[fullFilter]
        #######################################################################
        # Plot
        #######################################################################
        # Prepare the response surface ----------------------------------------
        (x, y, z) = (dfSrf[HD_IND[0]], dfSrf[HD_IND[1]], dfSrf[HD_DEP])
        rs = fun.calcResponseSurface(x, y, z, scalers=scalers, mthd=mthd)
        (rsG, rsS) = (rs['grid'], rs['surface'])
        # Plot the response surface -------------------------------------------
        fig, ax = plt.subplots()
        # Experiment points, contour lines, response surface
        xy = ax.plot(rsG[0], rsG[1], 'k.', ms=3, alpha=.25, marker='.')
        cc = ax.contour(rsS[0], rsS[1], rsS[2], levels=lvls, colors='w', linewidths=1, alpha=.5)
        cs = ax.contourf(rsS[0], rsS[1], rsS[2], levels=lvls, cmap=cmap, extend='max')
        # Figure Modifiers ----------------------------------------------------
        sz = fig.get_size_inches()[0]
        fig.set_size_inches(sz, .85*sz)
        # Colorbar
        cbar = fig.colorbar(cs)
        cbar.ax.get_yaxis().labelpad = 25
        cbar.ax.set_ylabel('{} (1/{})'.format(MOI, scalers[2]), fontsize=15, rotation=270)
        plt.xlabel(HD_IND[0], fontsize=20)
        plt.ylabel(HD_IND[1], fontsize=20)
        # Grid
        ax.grid(which='both', axis='y', lw=.5, alpha=.5, color=(0, 0, 0))
        ax.grid(which='both', axis='x', lw=.5, alpha=.5, color=(0, 0, 0))
        # Title
        xpStr = ['{}:{}'.format(i[0], str(i[1]).zfill(4)) for i in zip(hdFree, xpId)]
        ttlStr = ', '.join(xpStr)
        plt.title(ttlStr, fontsize=10, pad=10)
        # Filename and export
        xpStrNm = '_'.join([str(i).zfill(4) for i in xpId])
        xpFilename = xpStrNm+'_'+AOI+'_'+MOI
        fun.quickSaveFig(PT_IMG_XP+xpFilename, fig)
    print(monet.CEND, end='\r')
