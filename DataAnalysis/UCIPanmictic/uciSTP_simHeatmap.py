#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/23913151/log-log-lmplot-with-seaborn
# https://seaborn.pydata.org/generated/seaborn.heatmap.html
# https://matplotlib.org/3.2.1/gallery/images_contours_and_fields/irregulardatagrid.html
# https://matplotlib.org/3.2.1/gallery/images_contours_and_fields/contourf_demo.html#sphx-glr-gallery-images-contours-and-fields-contourf-demo-py

# import math
# import datetime
import numpy as np
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet
# import seaborn as sns
import uciPan_drive as drv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
# from matplotlib.colors import LinearSegmentedColormap

# cdict = {
#     'red':   ((0.0, 0.50, 0.50), (0.5, 0.5, 0.5), (1.0, 0.5, 0.5)),
#     'green': ((0.0, 0.00, 0.00), (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)),
#     'blue':  ((0.0, 0.25, 0.25), (0.5, 0.75, 0.75), (1.0, 1.0, 1.0)),
#     'alpha': ((0.0, 0.50, 0.50), (0.5, 0.50, 0.50), (1.0, 1.0, 1.0)),
# }
# cmap = LinearSegmentedColormap('Purple', cdict)

USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS, QNT, OVW) = (
        'gravidReleases', 'LDR', 'island', False,
        'HLT', (True, True), [.5, .95], False
    )
header = ['ratio', 'releases', 'fitness', 'sv', 'group']
(thr, sVar, REL_STRT, WRM) = (
        [int((1-i) * 100) for i in [.05, .10, .25, .50, .75]],
        [1, 5, 10, 50, 100, 500, 1000], 1, 0
    )
header.extend(thr)
drvPars = drv.driveSelector(DRV)
ci = QNT[1]
months = list(range(0, 78*4, 4))
(ngdx, ngdy) = (1000, 1000)
(xmin, xmax, ymin) = (10**-4, 1, 1)
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
PATH_IMG = PATH_DATA + 'img/'
monet.makeFolder(PATH_IMG)
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
            fName = 'RES-{}-{}-{}'.format(
                    str(level).zfill(3),
                    str(sv).zfill(4), str(group).zfill(3)
                )
            piv.to_csv(PATH_DATA+fName+'.csv')
            # Surfaces --------------------------------------------------------
            (x, y, z) = (df['ratio'], df['releases'], df[level])
            (x, y, z) = (
                    np.array([float(i/1000000) for i in x]),
                    np.array([int(i) for i in y]),
                    np.array([float(i) for i in z])
                )
            (a, b) = (max(x), max(y))
            (xi, yi) = (np.linspace(xmin, a, ngdx), np.linspace(xmin, b, ngdy))
            zi = griddata(
                    (x, y), z, (xi[None, :], yi[:, None]), method='linear'
                )
            # Plots
            fig, ax = plt.subplots()
            ax.plot(x, y, 'ko', ms=.5, alpha=.2)
            ax.contour(
                    xi, yi, zi,
                    levels=[4*i for i in [0, 8, 12, 24, 52, 78]],
                    linewidths=2, colors='k', alpha=.9
                )
            ax.contourf(
                    xi, yi, zi,
                    levels=[4*i for i in [0, 8, 12, 24, 52, 78]],
                    cmap='Purples'  # monet.cmaps[2]
                )
            ax.set(xscale="log", yscale="linear")
            sz = fig.get_size_inches()[0]
            fig.set_size_inches(sz, 1*sz)
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, b)
            plt.savefig(
                    PATH_IMG+fName+'.png',
                    dpi=400, facecolor=None, edgecolor='w',
                    orientation='portrait', papertype=None, format='png',
                    transparent=True, bbox_inches='tight', pad_inches=.01
                )
            plt.close('all')
