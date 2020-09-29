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
# Load folders
###############################################################################
exIx = 0
(pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx])
dirsTraces = monet.listDirectoriesWithPathWithinAPath(pathTraces)
humanFiles = [glob(i+'/H_*')[0] for i in dirsTraces]
hData = [np.loadtxt(i, skiprows=1, delimiter=',', usecols=(1, 2)) for i in humanFiles]

colors = ('#1b48e90B', '#ec114c0B')
(fig, ax) = plt.subplots(nrows=1, figsize=(10, 3))
for data in hData:
    (t, s) = data.shape
    total = np.sum(data, axis=1)
    for i in range(s):
        ax.plot(range(t), data[:,i]/total, lw=.1, color=colors[i])
fig.savefig(PT_IMG+'/test.png', dpi=750)
