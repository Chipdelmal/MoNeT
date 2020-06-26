#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from glob import glob
import svr_aux as aux
import svr_gene as drv
# import svr_functions as fun
# from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import compress_pickle as pkl
from scipy.interpolate import griddata

(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (True, True), [.5, .90, .95], True)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
(thr, REL_STRT, WRM, ci) = ([.05, .10, .25, .50, .75], 1, 0, QNT[1])
threshold = thr[0]
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
header = ['ratio', 'resistance', 'fitness', 'sv', 'group']
header.extend(thr)
drvPars = drv.driveSelector(DRV)
monet.makeFolder(PT_IMG)
months = list(range(0, 78*4, 4))
(ngdx, ngdy) = (1000, 1000)
###############################################################################
# Analyzes
###############################################################################
fPtrn = '{}/*{}*{}.csv'.format(PT_OUT, AOI, str(int(ci*100)))
fName = sorted(glob(fPtrn))[0]
df = pd.read_csv(fName, header=None, names=header)
(ratR, resR, fitR, svrR, grpP) = [list(df[i].unique()) for i in header[:5]]
# Filters ---------------------------------------------------------------------
(grpF, ratF) = ((df['group'] == 0),  (df['ratio'] == ratR[0]))

svrF = (df['sv'] == svrR[0])

filter = grpF & ratF & svrF
dff = df[filter]
# Surfaces --------------------------------------------------------
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
ax.plot(x, y, 'ko', ms=.5, alpha=.2)
ax.contour(
        xi, yi, zi,
        # levels=[4*i for i in [0, 8, 12, 24, 52, 78]],
        linewidths=2, colors='k', alpha=.9
    )
ax.contourf(
        xi, yi, zi,
        # levels=[4*i for i in [0, 8, 12, 24, 52, 78]],
        cmap='Purples'  # monet.cmaps[2]
    )
ax.set(xscale="linear", yscale="linear")
sz = fig.get_size_inches()[0]
fig.set_size_inches(sz, 1*sz)
plt.xlim(a[0], a[1])
plt.ylim(b[0], b[1])
