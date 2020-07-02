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

(USR, DRV, AOI) = (sys.argv[1], 'replacement', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (True, True), [.05], True)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, True)
(thr, REL_STRT, WRM, ci) = ([.05, .10, .25, .50, .75], 1, 0, QNT[0])
(threshold, lvls) = (thr[0], 7)
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
header = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group']
header.extend(thr)
drvPars = drv.driveSelector(DRV)
monet.makeFolder(PT_IMG)
(ngdx, ngdy) = (1000, 1000)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Heatmap ' + AOI)
###############################################################################
# Analyzes
###############################################################################
for threshold in thr:
    fPtrn = '{}/*{}*{}-WOP.csv'.format(PT_OUT, AOI, str(int(ci*100)))
    fName = sorted(glob(fPtrn))[0]
    df = pd.read_csv(fName, header=None, names=header)
    (ratR, rnm, resR, fitR, svrR, grpP) = [list(df[i].unique()) for i in header[:6]]
    for svr in svrR:
        # Filters -------------------------------------------------------------
        (grpF, ratF) = ((df['group'] == 0), (df['ratio'] == ratR[0]))
        (svrF, relF) = ((df['sv'] == svr), df['releases'] == 1)
        filter = grpF & ratF & svrF
        dff = df[filter]
        # Surfaces ------------------------------------------------------------
        (x, y, z) = (df['resistance'], df['fitness'], df[threshold])
        (x, y, z) = (
                np.array([float(i/1000000) for i in x]),
                np.array([float(i/1000000) for i in y]),
                np.array([float(i) for i in z])
            )
        (a, b) = ((min(x), max(x)), (min(y), max(y)))
        (xi, yi) = (np.linspace(a[0], a[1], ngdx), np.linspace(b[0], b[1], ngdy))
        zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='linear')
        # Plots
        fig, ax = plt.subplots()
        ax.plot(x, y, 'ko', ms=1, alpha=.5, marker='x')
        ax.contour(
                xi, yi, zi, levels=lvls,
                linewidths=2, colors='k', alpha=.9
            )
        htmp = ax.contourf(xi, yi, zi, levels=lvls, cmap='Purples')
        ax.set(xscale="log", yscale="linear")
        ax.set_xlabel('R Generation', fontsize=22.5)
        ax.set_ylabel('Fitness Cost', fontsize=22.5)
        sz = fig.get_size_inches()[0]
        fig.set_size_inches(sz, 1*sz)
        plt.xlim(0.000001, a[1])
        plt.ylim(b[0], b[1])
        plt.title(
                str(int((1-threshold)*100))+'% window of protection\n',
                fontsize=30
            )
        cbar = plt.colorbar(htmp, pad=0.01)
        fig.savefig(
                "{}/HT-{}-{}.png".format(
                        PT_IMG, str(int(threshold*100)).zfill(3),
                        str(svr).zfill(10)
                    ),
                dpi=250, facecolor=None, edgecolor='w',
                orientation='portrait', papertype=None, format='png',
                transparent=True, bbox_inches='tight', pad_inches=.01
            )
        plt.close('all')
