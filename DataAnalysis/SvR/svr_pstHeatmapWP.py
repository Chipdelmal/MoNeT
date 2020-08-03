#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
# import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import compress_pickle as pkl
from scipy.interpolate import griddata


(USR, DRV, AOI, WLA) = (sys.argv[1], sys.argv[2], 'HLT', sys.argv[3])
# (USR, DRV, AOI) = ('dsk', 'HH', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (False, True), [.05, .1, .5], True)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, True)
(thr, REL_STRT, WRM, ci) = ([.05, .10, .25, .50, .75], 1, 0, QNT[0])
(threshold, lvls, mthd, xSca) = (thr[1], 10, 'nearest', 'log')
mapLevels = np.arange(0, 3*365, 50)
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
header = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group']
header.extend(thr)
drvPars = drv.driveSelector(DRV)
PT_IMG = PT_IMG[:-5] + '/htmps/'
monet.makeFolder(PT_IMG)
(ngdx, ngdy) = (1000, 1000)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Heatmap ' + AOI)
###############################################################################
# Analyzes
###############################################################################
msg = '* Analyzing ({}/{})'
for (i, threshold) in enumerate(thr):
    print(msg.format(i+1, len(thr)), end='\r')
    fPtrn = '{}/*{}*{}-{}.csv'.format(PT_OUT, AOI, str(int(ci*100)), WLA)
    fName = sorted(glob(fPtrn))[0]
    df = pd.read_csv(fName, header=None, names=header)
    (ratR, rnm, resR, fitR, svrR, grpP) = [list(df[i].unique()) for i in header[:6]]
    for res in resR:
        # Filters -------------------------------------------------------------
        (grpF, ratF) = ((df['group'] == 0), (df['ratio'] == ratR[0]))
        (resF, relF) = ((df['resistance'] == res), df['releases'] == 1)
        filter = grpF & ratF & resF & relF
        dff = df[filter]
        # Surfaces ------------------------------------------------------------
        (x, y, z) = (dff['sv'], dff['fitness'], dff[threshold])
        (x, y, z) = (
                np.array([float(i/100000000) for i in x]),
                np.array([float(i/100000000) for i in y]),
                np.array([float(i) for i in z])
            )
        (a, b) = ((min(x), max(x)), (min(y), max(y)))
        (xi, yi) = (
                np.linspace(a[0], a[1], ngdx), np.linspace(b[0], b[1], ngdy)
            )
        zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method=mthd)
        # Plots Label ---------------------------------------------------------
        fig, ax = plt.subplots()
        ax.plot(x, y, 'k.', ms=1, alpha=.25, marker='.')
        ax.contour(
                xi, yi, zi, levels=mapLevels,
                linewidths=.5, colors='k', alpha=.5,
            )
        htmp = ax.contourf(
                xi, yi, zi, levels=mapLevels,
                cmap=aux.cmapB, extend='max'
            )
        htmp.cmap.set_over('#090446')
        ax.set(xscale=xSca, yscale="linear")
        ax.set_xlabel('Standing Variation', fontsize=22.5)
        ax.set_ylabel('Fitness Cost', fontsize=22.5)
        sz = fig.get_size_inches()[0]
        fig.set_size_inches(sz, 1*sz)
        # Axes
        ax.set_xticks(list(set(x)), minor=True)
        ax.set_xticklabels([], minor=True)
        ax.set_yticks(list(set(y)), minor=True)
        ax.set_yticklabels([], minor=True)
        ax.grid(which='both', axis='y', lw=.1, alpha=0.1, color=(0, 0, 0))
        ax.grid(which='minor', axis='x', lw=.1, alpha=0.1, color=(0, 0, 0))
        # Limits
        plt.xlim(1E-6, 1E-1)
        plt.ylim(b[0], b[1])
        plt.title(
                '{}% window of protection \nR: {:.2e}\n'.format(
                        int((1-threshold)*100), res / 100000000
                    ),
                fontsize=20
            )
        cbar = plt.colorbar(htmp, pad=0.01)
        fig.savefig(
             "{}/HL-{}-{}-{}.png".format(
                     PT_IMG, WLA, str(int(threshold*100)).zfill(3),
                     str(res).zfill(10)
                 ),
             dpi=750, facecolor=None, edgecolor='w',
             orientation='portrait', papertype=None, format='png',
             transparent=True, bbox_inches='tight', pad_inches=.01
         )
        plt.close('all')
        # Plots NL-------------------------------------------------------------
        fig, ax = plt.subplots()
        ax.plot(x, y, 'k.', ms=1, alpha=.25, marker='.')
        ax.contour(
                xi, yi, zi, levels=mapLevels,
                linewidths=.5, colors='k', alpha=.5,
            )
        htmp = ax.contourf(
                xi, yi, zi, levels=mapLevels,
                cmap=aux.cmapB, extend='max'
            )
        htmp.cmap.set_over('#090446')
        ax.set(xscale=xSca, yscale="linear")
        sz = fig.get_size_inches()[0]
        fig.set_size_inches(sz, 1*sz)
        # Axes
        ax.set_xticks(list(set(x)), minor=True)
        ax.set_yticks(list(set(y)), minor=True)
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.axes.xaxis.set_ticklabels([], minor=True)
        ax.axes.yaxis.set_ticklabels([], minor=True)
        ax.grid(which='both', axis='y', lw=.1, alpha=0.1, color=(0, 0, 0))
        ax.grid(which='minor', axis='x', lw=.1, alpha=0.1, color=(0, 0, 0))
        # Limits
        plt.xlim(1E-6, 1E-1)
        plt.ylim(b[0], b[1])
        fig.savefig(
             "{}/HS-{}-{}-{}.png".format(
                     PT_IMG, WLA, str(int(threshold*100)).zfill(3),
                     str(res).zfill(10)
                 ),
             dpi=750, facecolor=None, edgecolor='w',
             orientation='portrait', papertype=None, format='png',
             transparent=True, bbox_inches='tight', pad_inches=.01
         )
        plt.close('all')
print('* Analyzed ({}/{})                         '.format(len(thr), len(thr)))
print(monet.PAD)