#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from glob import glob
import svr_aux as aux
import svr_gene as drv
# import svr_functions as fun
# from datetime import datetime
import MoNeT_MGDrivE as monet
# import compress_pickle as pkl

(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (True, True), [.5, .95], True)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
(thr, REL_STRT, WRM, ci) = ([.05, .10, .25, .50, .75], 1, 0, QNT[1])
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
header = ['ratio', 'resistance', 'fitness', 'sv', 'group']
header.extend(thr)
drvPars = drv.driveSelector(DRV)
monet.makeFolder(PT_IMG)
months = list(range(0, 78*4, 4))
(ngdx, ngdy) = (1000, 1000)
(xmin, xmax, ymin) = (10**-4, 1, 1)
###############################################################################
# Analyzes
###############################################################################
fPtrn = '{}/*{}.csv'.format(PT_OUT, str(int(ci*100)))
fName = sorted(glob(fPtrn))[0]
df = pd.read_csv(fName, header=None, names=header)
xpHdrSets = [list(df[i].unique()) for i in header[:5]]

# for sv in sVar:
#     for level in thr:
#         # Loading filenames
#         fNames = sorted(glob('{}*_{}.csv'.format(
#                 PATH_DATA, str(int(ci*100))))
#             )
#         raw = pd.read_csv(fNames[0], header=None, names=header)
#         # Seeding dataframe
#         filter = (raw['group'] == group) & (raw['sv'] == sv)
#         df = raw[filter]
#         # Appending elements
#         for i in range(1, len(fNames)):
#             fNames = sorted(glob('{}*{}.csv'.format(
#                     PATH_DATA, str(int(ci*100))))
#                 )
#             raw = pd.read_csv(fNames[i], header=None, names=header)
#             df = df.append(raw[filter])
#         # Pivot the table
#         piv = df.pivot('releases', 'ratio', level)
#         fName = 'RES-{}-{}-{}'.format(
#                 str(level).zfill(3),
#                 str(sv).zfill(4), str(group).zfill(3)
#             )
#         piv.to_csv(PATH_DATA+fName+'.csv')
#         # Surfaces --------------------------------------------------------
#         (x, y, z) = (df['ratio'], df['releases'], df[level])
#         (x, y, z) = (
#                 np.array([float(i/1000000) for i in x]),
#                 np.array([int(i) for i in y]),
#                 np.array([float(i) for i in z])
#             )
#         (a, b) = (max(x), max(y))
#         (xi, yi) = (np.linspace(xmin, a, ngdx), np.linspace(xmin, b, ngdy))
#         zi = griddata(
#                 (x, y), z, (xi[None, :], yi[:, None]), method='linear'
#             )
#         # Plots
#         fig, ax = plt.subplots()
#         ax.plot(x, y, 'ko', ms=.5, alpha=.2)
#         ax.contour(
#                 xi, yi, zi,
#                 levels=[4*i for i in [0, 8, 12, 24, 52, 78]],
#                 linewidths=2, colors='k', alpha=.9
#             )
#         ax.contourf(
#                 xi, yi, zi,
#                 levels=[4*i for i in [0, 8, 12, 24, 52, 78]],
#                 cmap='Purples'  # monet.cmaps[2]
#             )
#         ax.set(xscale="log", yscale="linear")
#         sz = fig.get_size_inches()[0]
#         fig.set_size_inches(sz, 1*sz)
#         plt.xlim(xmin, xmax)
#         plt.ylim(ymin, b)
#         plt.savefig(
#                 PATH_IMG+fName+'.png',
#                 dpi=400, facecolor=None, edgecolor='w',
#                 orientation='portrait', papertype=None, format='png',
#                 transparent=True, bbox_inches='tight', pad_inches=.01
#             )
#         plt.close('all')
