
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import STP_functions as fun
import STP_plots as plo
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D


plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
})




PTH_pts = '/media/hdd/WorkExperiments/STP/'
pts = pd.read_csv(PTH_pts+'stp_all_sites_v5.csv')
COLORS = plo.COLORS
# #############################################################################
# Sao Tome
# #############################################################################
(minLat, minLong) = (-0.045, 6.4)
(maxLat, maxLong) = (.5, 6.8)
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
mH = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='h', ax=ax
)
mH.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
mH.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=2)
mL = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=COLORS[4], linewidth=10, zorder=0)
ax.tick_params(
    axis='both', which='both',
    bottom=True, top=False, left=True, right=False,
    labelbottom=True, labelleft=True
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
mH.scatter(
    list(pts['lon']), list(pts['lat']), latlon=True,
    alpha=.2, marker='.', s=[10 * math.log(i) for i in list(pts['pop'])],
    color='#E048B8', zorder=3
)
fun.quickSaveFig(PTH_pts + 'ST.png', fig, dpi=750)
# #############################################################################
# Principe
# #############################################################################
(minLat, minLong) = (1.5, 7.275)
(maxLat, maxLong) = (1.75, 7.5)
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
mH = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='h', ax=ax
)
mH.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
mH.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=2)
mL = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=COLORS[4], linewidth=10, zorder=0)
ax.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=True, labelleft=True
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
mH.scatter(
    list(pts['lon']), list(pts['lat']), latlon=True,
    alpha=.2, marker='.', s=[10 * math.log(i) for i in list(pts['pop'])],
    color='#E048B8', zorder=5
)
fun.quickSaveFig(PTH_pts + 'PP.png', fig, dpi=750)
# #############################################################################
# Globe
# #############################################################################
(x1, y1) = (6.602781, 0.255436)
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
map = Basemap(projection='ortho', lat_0=y1, lon_0=x1-20, ax=ax, resolution='c')
# map = Basemap(projection='geos', lon_0=-89.5, lat_0=0.0, satellite_height=45786023.0, ellps='GRS80')
map.drawmapboundary(color=COLORS[3], linewidth=5, zorder=5, ax=ax)
pad = 500000
(limx, limy) = (ax.get_xlim(), ax.get_ylim())
ax.set_xlim(limx[0] - pad, limx[1] + pad)
ax.set_ylim(limy[0] - pad, limy[1] + pad)
# map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color="#ffffff", lake_color="#ffffff00")
# map.drawcoastlines()
map.drawcoastlines(color=COLORS[3], linewidth=0)
# map.drawcoastlines(color=COLORS[0], linewidth=2)
map.drawcoastlines(color=COLORS[3], linewidth=0.25)
map.drawparallels(np.arange(-90., 120., 30.), labels=[1,0,0,0], color='w', linewidth=.2)
map.drawmeridians(np.arange(0., 420., 60.), labels=[0,0,0,1], color='w',  linewidth=.2)
(x, y) = map(x1, y1)
map.plot(x, y, marker='o', color="#e048b8F5")
fun.quickSaveFig(PTH_pts + 'GB.png', fig, dpi=750)
