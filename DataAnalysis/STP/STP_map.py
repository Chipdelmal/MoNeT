
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
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D



def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


COLORS = [
        rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        rescaleRGBA((255, 0, 152, 255/1)),      # 1: Magenta
        rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]


PTH_pts = '/media/hdd/WorkExperiments/STP/'
pts = pd.read_csv(PTH_pts+'stp_all_sites_v5.csv')


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
    color='#E048B8', zorder=3
)
fun.quickSaveFig(PTH_pts + 'PP.png', fig, dpi=750)
