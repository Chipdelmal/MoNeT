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
###############################################################################
# Genotypes
###############################################################################
genes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
locs = {
        'H': (('H', (0, 1)), ),
        'O': (('W', (0, 1)), ('R', (0, 1)), ('B', (0, 1)))
    }
hset = set(aux.aggregateGeneAppearances(genes, locs['H']))
oset = set(aux.aggregateGeneAppearances(genes, locs['O']))
healthSet = (hset, oset-hset, oset | hset)
HLT = monet.generateAggregationDictionary(
        ["H", "W", "Total"], [list(i) for i in healthSet]
    )
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
mID = ('FS', 'FE', 'FI')
mPops = {}
for id in mID:
    FIfiles = [glob(i+'/'+id+'*.csv')[0] for i in dirsTraces]
    pops = []
    for file in FIfiles:
        dta = np.loadtxt(file, skiprows=1, delimiter=',', usecols=(1, ))
        nodeData = monet.loadNodeData(femaleFilename=file)
        pop = monet.aggregateGenotypesInNode(nodeData, HLT)['population']
        pops.append(pop)
    mPops[id] = pops
# Populations summed into one node (disregards infection status) --------------
sums = []
for r in range(len(dirsTraces)):
    sums.append(mPops['FS'][r] + mPops['FE'][r] + mPops['FI'][r])
###############################################################################
# Plot
###############################################################################
# Human -----------------------------------------------------------------------
colors = ('#6347ff0C', '#e6303f0C')
(fig, ax) = plt.subplots(nrows=1, figsize=(10, 3))
for data in hData:
    (t, s) = data.shape
    total = np.sum(data, axis=1)
    for i in range(s):
        ax.plot(range(t), data[:, i]/total, lw=.5, color=colors[i])
# Mosquito --------------------------------------------------------------------
colors = ('#B8B8FF15', '#E64E5B15')
for rep in sums:
    frac = [aux.zeroDivide(i, rep[:, 2]) for i in (rep[:, 0], rep[:, 1])]
    ax.plot(range(t), frac[0], lw=.4, ls='--', color=colors[0])
    ax.plot(range(t), frac[1], lw=.4, ls='--', color=colors[1])
infected = [i[:, 2] for i in mPops['FI']]
for inf in infected:
    ax.plot(range(t), aux.zeroDivide(inf, total), lw=.5, color='#A613800A')
# Other important lines -------------------------------------------------------
# ax.axvspan(3*365, days, color='#0A1CC2', alpha=.03)
ax.axvspan(0, 3*365, color='#544496', alpha=.025)
for i in [1095, 1102, 1109, 1116, 1123, 1130, 1137, 1144]:
    ax.axvline(i, alpha=.35, lw=.2, color='black')
# Grid and limits -------------------------------------------------------------
ax.set_xticks(np.arange(0, days, 365))
ax.set_yticks(np.arange(0, 1.05, 0.25))
ax.axes.set_xlim(0, days)
ax.axes.set_ylim(-.0035, 1.0035)
plt.grid(alpha=.25, lw=.5)
# Save figure -----------------------------------------------------------------
fig.savefig(PT_IMG+'/test.png', dpi=750, bbox_inches='tight', pad_inches=.05)


locsE = {
        'H': (('H', (0, 1)), ),
        'W': (('W', (0, 1)), ),
        'R': (('R', (0, 1)), ('B', (0, 1)))
    }
hlst = aux.aggregateGeneAppearances(genes, locsE['H'])
wlst = aux.aggregateGeneAppearances(genes, locsE['W'])
rlst = aux.aggregateGeneAppearances(genes, locsE['R'])
ECO = monet.generateAggregationDictionary(
        ["H", "W", "R"], [hlst, wlst, rlst]
    )
# Mosquito files --------------------------------------------------------------
mID = ('FS', 'FE', 'FI')
mPopsECO = {}
for id in mID:
    FIfiles = [glob(i+'/'+id+'*.csv')[0] for i in dirsTraces]
    pops = []
    for file in FIfiles:
        dta = np.loadtxt(file, skiprows=1, delimiter=',', usecols=(1, ))
        nodeData = monet.loadNodeData(femaleFilename=file)
        pop = monet.aggregateGenotypesInNode(nodeData, ECO)['population']
        pops.append(pop)
    mPopsECO[id] = pops
# Populations summed into one node (disregards infection status) --------------
sumsECO = []
for r in range(len(dirsTraces)):
    sumsECO.append(mPopsECO['FS'][r] + mPopsECO['FE'][r] + mPopsECO['FI'][r])
