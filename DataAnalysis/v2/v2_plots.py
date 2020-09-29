#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import matplotlib
import numpy as np
from glob import glob
import v2_aux as aux
import v2_land as lnd
import v2_gene as drv
import v2_framework as frame
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


(USR, DRV, AOI) = ('dsk', 'LDR', 'HLT')
(OVW, MF, JOB) = (True, (False, True), 1)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, False)
(PT_ROT, PT_PRE, PT_OUT, PT_IMG, PT_MTR) = aux.selectPath(USR)
(expDirsMean, expDirsTrac) = aux.getExpPaths(PT_ROT)
genes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
locs = {
        'H': (('H', (0, 1)), ),
        'O': (('W', (0, 1)), ('R', (0, 1)), ('B', (0, 1)))
    }
hset = set(aux.aggregateGeneAppearances(genes, locs['H']))
oset = set(aux.aggregateGeneAppearances(genes, locs['O']))
HLT = (hset, oset-hset, oset | hset)
###############################################################################
# Load folders
###############################################################################
exIx = 0
(pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx])
dirsTraces = monet.listDirectoriesWithPathWithinAPath(pathTraces)
# Human files -----------------------------------------------------------------
humanFiles = [glob(i+'/H_*')[0] for i in dirsTraces]
hData = [np.loadtxt(i, skiprows=1, delimiter=',', usecols=(1, 2)) for i in humanFiles]
(days, states) = hData[0].shape
# Mosquito files --------------------------------------------------------------
FIfiles = [glob(i+'/FI*.csv')[0] for i in dirsTraces]
genotypes = monet.readGenotypes(FIfiles[0])
genes = [i.replace('\"', '').replace('\n', '') for i in genotypes]
dta = np.loadtxt(FIfiles[0], skiprows=1, delimiter=',', usecols=(1, ))

genes
monet.loadAndAggregateLandscapeData(FIfiles[0])
###############################################################################
# Plot
###############################################################################
colors = ('#1b48e90B', '#ec114c0B')
(fig, ax) = plt.subplots(nrows=1, figsize=(10, 3))
for data in hData:
    (t, s) = data.shape
    total = np.sum(data, axis=1)
    for i in range(s):
        ax.plot(range(t), data[:, i]/total, lw=.25, color=colors[i])
# Grid and limits -------------------------------------------------------------
ax.set_xticks(np.arange(0, days, 365))
ax.set_yticks(np.arange(0, 1.05, 0.25))
ax.axes.set_xlim(0, days)
ax.axes.set_ylim(0, 1.0)
plt.grid()
fig.savefig(PT_IMG+'/test.png', dpi=750, bbox_inches='tight', pad_inches=.05)
