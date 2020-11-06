#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import warnings
import STP_aux as aux
import STP_functions as fun
from itertools import product
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


# (USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(USR, AOI, REL, LND, MOI) = ('dsk', 'HLT', 'mixed', 'PAN', 'WOP')
(DRV, FMT, QNT, OVW) = ('LDR', 'bz2', '50', True)
# Select surface variables ----------------------------------------------------
HD_IND = ['i_ren', 'i_fic']
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI, AOI)
(ngdx, ngdy) = (5000, 5000)
(lvls, mthd, xSca, ySca) = (
        [-.1, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1, 1.1],
        'linear', 'linear', 'linear'
    )
xRan = (1E-8, 1E-1)
# Patch scalers for experiment id ---------------------------------------------
sclr = [1e8, 1e8, scalers[2]]
if 'i_ren' in HD_IND:
    sclr[HD_IND.index('i_ren')] = 1
###############################################################################
# Setup paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
PT_IMG = PT_IMG + 'heat/'
monet.makeFolder(PT_IMG)
PT_IMG = PT_IMG+'-'.join(HD_IND)+'/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_MTR, tS, 'Heatmap '+AOI)
###########################################################################
# Analyzes
###########################################################################
# Load files into dataframe
fPtrn = '{}{}_{}_{}_qnt.csv'.format(PT_MTR, AOI, MOI, QNT)
(df, header, headerInd) = monet.loadDFFromSummary(fPtrn)
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
###########################################################################
# Analyzes
###########################################################################
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
    (a, b) = ((min(x), max(x)), (min(y), max(y)))
    rs = fun.calcResponseSurface(x, y, z, scalers=sclr, mthd=mthd)
    (rsG, rsS) = (rs['grid'], rs['surface'])
    # Plot the response surface -------------------------------------------
    (fig, ax) = plt.subplots(figsize=(8, 7))
    # Experiment points, contour lines, response surface
    xy = ax.plot(rsG[0], rsG[1], 'k.', ms=3, alpha=.25, marker='.')
    cc = ax.contour(rsS[0], rsS[1], rsS[2], levels=lvls, colors='w', linewidths=1, alpha=.5)
    cs = ax.contourf(rsS[0], rsS[1], rsS[2], levels=lvls, cmap=cmap, extend='max')
    # Figure Modifiers ----------------------------------------------------
    # cs.cmap.set_over('#000000')
    sz = fig.get_size_inches()[0]
    # ax.set(xscale=xSca, yscale="linear")
    # Colorbar
    cbar = fig.colorbar(cs)
    cbar.ax.get_yaxis().labelpad = 25
    cbar.ax.set_ylabel('{} (1/{})'.format(MOI, sclr[2]), fontsize=15, rotation=270)
    plt.xlabel(HD_IND[0], fontsize=20)
    plt.ylabel(HD_IND[1], fontsize=20)
    # Grid
    # ax.set_xscale(xSca)
    # ax.set_yscale(ySca)
    ax.set_xticks([i/sclr[0] for i in list(set(x))], minor=True)
    ax.set_yticks([i/sclr[1] for i in list(set(y))], minor=True)
    # ax.axes.xaxis.set_ticklabels([])
    # ax.axes.yaxis.set_ticklabels([])
    # ax.axes.xaxis.set_ticklabels([], minor=True)
    # ax.axes.yaxis.set_ticklabels([], minor=True)
    ax.grid(which='both', axis='y', lw=.1, alpha=0.1, color=(0, 0, 0))
    ax.grid(which='minor', axis='x', lw=.1, alpha=0.1, color=(0, 0, 0))
    # Limits
    # plt.xlim(xRan[0], xRan[1])
    # plt.ylim(b[0], b[1])
    # Title
    xpStr = [
        '{}:{}'.format(i[0], str(i[1]).zfill(4)) for i in zip(hdFree, xpId)
    ]
    ttlStr = ', '.join(xpStr)
    plt.title(ttlStr, fontsize=10, pad=10)
    # Filename and export
    xpStrNm = '_'.join([str(i).zfill(4) for i in xpId])
    xpFilename = xpStrNm+'_'+AOI+'_'+MOI+'.png'
    fun.quickSaveFig(PT_IMG+xpFilename, fig)
    plt.close('all')
print(monet.CEND, end='\r')
