#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import warnings
import tGD_aux as aux
import tGD_fun as fun
from itertools import product
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
# ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']

# python tGD_pstHeatmapSSV.py srv linkedDrive HLT WOP
(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, DRV, AOI, MOI) = ('dsk', 'tGD', 'WLD', 'MNX')
(FMT, SKP, MF,  OVW, QNT) = ('bz', False, (False, True), True, '50')
# Select surface variables ----------------------------------------------------
HD_IND = ['i_ren', 'i_hnf']
(ngdx, ngdy) = (1000, 1000)
(lvls, mthd, xSca, ySca) = (
        [-.05, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1],
        'linear', 'linear', 'linear'
    )
MOI = ('TTI', 'TTO', 'WOP', 'MNX', 'RAP')
for moi in MOI:
    (scalers, HD_DEP, _, cmapR) = aux.selectDepVars(moi, AOI)
    cmap = cmapR.reversed()
    # Spatial settings to sweep through ---------------------------------------
    EXPS = ('000', ) # '001', '005', '010', '100')
    ###########################################################################
    # Loop through the experiments
    ###########################################################################
    for exp in EXPS:
        (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
        PT_IMG = PT_IMG + 'heat/'
        monet.makeFolder(PT_IMG)
        PT_IMG = PT_IMG+'-'.join(HD_IND)+'/'
        monet.makeFolder(PT_IMG)
        tS = datetime.now()
        aux.printExperimentHead(PT_ROT, PT_IMG, PT_MTR, tS, 'Heatmap '+AOI)
        #######################################################################
        # Analyzes
        #######################################################################
        # Load files into dataframe
        fPtrn = '{}{}_{}_{}_qnt.csv'.format(PT_MTR, AOI, moi, QNT)
        (df, header, headerInd) = aux.loadDFFromSummary(fPtrn)
        # Filter the dataframe ------------------------------------------------
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
            ###################################################################
            # Filter
            ###################################################################
            indepFltrs = [list(df[hId[1]] == hId[0]) for hId in zip(xpId, hdFree)]
            fullFilter = list(map(all, zip(*indepFltrs)))
            dfSrf = df[fullFilter]
            ###################################################################
            # Plot
            ###################################################################
            # Prepare the response surface ------------------------------------
            (x, y, z) = (dfSrf[HD_IND[0]], dfSrf[HD_IND[1]], dfSrf[HD_DEP])
            # if moi == 'MNX':
            #     z = [i for i in z]
            #     print(list(z))
            rs = fun.calcResponseSurface(x, y, z, scalers=scalers, mthd=mthd)
            (rsG, rsS) = (rs['grid'], rs['surface'])
            # Plot the response surface ---------------------------------------
            fig, ax = plt.subplots()
            # Experiment points, contour lines, response surface
            xy = ax.plot(rsG[0], rsG[1], 'k.', ms=3, alpha=.25, marker='.')
            cc = ax.contour(rsS[0], rsS[1], rsS[2], levels=lvls, colors='w', linewidths=1, alpha=.5)
            cs = ax.contourf(rsS[0], rsS[1], rsS[2], levels=lvls, cmap=cmap, extend='max')
            # Figure Modifiers ------------------------------------------------
            sz = fig.get_size_inches()[0]
            fig.set_size_inches(sz, .85*sz)
            ax.set_xscale(xSca)
            ax.set_yscale(ySca)
            # Colorbar
            cbar = fig.colorbar(cs)
            cbar.ax.get_yaxis().labelpad = 25
            cbar.ax.set_ylabel('{} (1/{})'.format(moi, scalers[2]), fontsize=15, rotation=270)
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
            xpFilename = xpStrNm+'_'+AOI+'_'+moi
            fun.quickSaveFig(PT_IMG+xpFilename+'-'+QNT+'.png', fig)
        print(monet.CEND, end='\r')
