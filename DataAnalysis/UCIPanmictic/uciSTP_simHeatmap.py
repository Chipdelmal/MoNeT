#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/23913151/log-log-lmplot-with-seaborn
# https://seaborn.pydata.org/generated/seaborn.heatmap.html
# https://matplotlib.org/3.2.1/gallery/images_contours_and_fields/irregulardatagrid.html
# https://matplotlib.org/3.2.1/gallery/images_contours_and_fields/contourf_demo.html#sphx-glr-gallery-images-contours-and-fields-contourf-demo-py

import math
# import datetime
import numpy as np
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet
# import seaborn as sns
import uciPan_drive as drv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS, QNT, OVW) = (
        'gravidReleases', 'LDR', 'island', False,
        'HLT', (True, True), [.5, .9, .95], False
    )
header = ['ratio', 'releases', 'fitness', 'sv', 'group']
(thr, sVar, REL_STRT, WRM) = (
        [int((1-i) * 100) for i in [.05, .10, .25, .50, .75]],
        [1, 5, 10, 50, 100, 500, 1000], 1, 0
    )
header.extend(thr)
drvPars = drv.driveSelector(DRV)
ci = QNT[2]
months = list(range(0, 12*4, 6))
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
            # Plot
            (x, y, z) = (df['ratio'], df['releases'], df[level])
            (x, y, z) = (
                    np.array([float(i/1000000) for i in x]),
                    np.array([int(i) for i in y]),
                    np.array([float(i) for i in z])
                )
            (a, b) = (max(x), max(y))
            fig, ax = plt.subplots()
            ax.tricontourf(
                    x, y, z,
                    levels=[4*i for i in months],
                    cmap="PuBu"
                )
            ax.set(xscale="log", yscale="linear")
            fig.set_size_inches(
                    fig.get_size_inches()[0],
                    1*fig.get_size_inches()[0]
                )
            plt.savefig(
                    PATH_IMG+fName+'.png',
                    dpi=400, facecolor=None, edgecolor='w',
                    orientation='portrait', papertype=None, format='png',
                    transparent=True, bbox_inches='tight', pad_inches=.01
                )
            plt.close('all')



###############################################################################
# Heatmap
###############################################################################
# (x, y, z) = (df['releases'], df['ratio'], df[level])
# (x, y, z) = (
#         np.array([int(i) for i in x]),
#         np.array([float(i/1000000) for i in y]),
#         np.array([float(i) for i in z])
#     )
#(ngridx, ngridy) = (1000, 1000)
# (grid_x, grid_y) = np.mgrid[0:a:100j, 0:b:200j]
# grid = griddata((x, y), z, (grid_x, grid_y), method='nearest')
# fig, ax = plt.subplots()
# ax.tricontourf(x, y, z, levels=10, cmap="RdBu_r")
# ax.set(xscale="log", yscale="linear")
# xmin, xmax = ax.get_xbound()
# ymin, ymax = ax.get_ybound()
# data_aspect = (
#     math.log(ymax)-math.log(ymin))/(math.log(xmax)-math.log(xmin)
#     )
# # ax.set_aspect(1./data_aspect)
# fig_ratio=1
# fig.set_size_inches(fig.get_size_inches()[0], fig_ratio*fig.get_size_inches()[0])
#
#
#
# (xi, yi) = (np.linspace(0, a, ngridx), np.linspace(0, b, ngridy))
# fig, ax = plt.subplots()
# zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='linear')
# ax.contour(xi, yi, zi, levels=14, linewidths=1, colors='k')
# ax.set(xscale="log", yscale="linear")
# cntr1 = ax.contourf(xi, yi, zi, levels=14, cmap="RdBu_r")
# fig.set_size_inches(fig.get_size_inches()[0], fig_ratio*fig.get_size_inches()[0])
