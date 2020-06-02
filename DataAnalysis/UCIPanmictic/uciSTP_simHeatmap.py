#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/23913151/log-log-lmplot-with-seaborn
# https://seaborn.pydata.org/generated/seaborn.heatmap.html

# import datetime
import numpy as np
import pandas as pd
from glob import glob
# import seaborn as sns
import uciPan_drive as drv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS, QNT, OVW) = (
        'tParams', 'LDR', 'island', False,
        'HLT', (True, True), [.5, .9, .95], False
    )
header = ['ratio', 'releases', 'fitness', 'sv', 'group']
(thr, sVar, REL_STRT, WRM) = (
        [int((1-i) * 100) for i in [.05, .10, .25, .50, .75]],
        [1, 5, 10, 50, 100, 500, 1000],
        1, 0
    )
header.extend(thr)
drvPars = drv.driveSelector(DRV)
ci = QNT[2]
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/{}/'.format(LND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/Panmictic/{}/{}/'.format(
        LND, SET)
PATH_DATA = '{}out/LDR/POSTPROCESS/'.format(PATH_ROOT)
###############################################################################
# Analyzes
###############################################################################
for group in [0]:
    for sv in sVar:
        for level in thr:
            # Loading filenames
            fNames = sorted(glob('{}*_{}.csv'.format(
                    PATH_DATA, str(int(ci*100))))
                )
            raw = pd.read_csv(fNames[0], header=None, names=header)
            # Seeding dataframe
            filter = (raw['group'] == group) & (raw['sv'] == sv)
            df = raw[filter]
            # Appending elements
            for i in range(1, len(fNames)):
                fNames = sorted(glob('{}*{}.csv'.format(
                        PATH_DATA, str(int(ci*100))))
                    )
                raw = pd.read_csv(fNames[i], header=None, names=header)
                df = df.append(raw[filter])
            # Pivot the table
            piv = df.pivot('releases', 'ratio', level)
            piv.to_csv(
                    '{}RES-{}-{}-{}.csv'.format(
                            PATH_DATA, str(level).zfill(3),
                            str(sv).zfill(4), str(group).zfill(3)
                    )
                )
###############################################################################
# Heatmap
###############################################################################
# f, ax = plt.subplots(figsize=(7, 7))
# ax.set(xscale="log", yscale="linear")
# ax.invert_yaxis()
# ax = sns.heatmap(piv, cmap="Blues")
(x, y, z) = (df['releases'], df['ratio'], df[level])
(x, y, z) = (
        np.array([int(i) for i in x]),
        np.array([int(i) for i in y]),
        np.array([float(i) for i in z])
    )
(grid_x, grid_y) = np.mgrid[0:52:100j, 0:1000000:200j]
grid = griddata((x, y), z, (grid_x, grid_y), method='nearest')
ax = plt.subplot(222)
plt.imshow(grid.T, extent=(0, 52, 0, 1000000), origin='lower')
ax.set_aspect(1/20000)
