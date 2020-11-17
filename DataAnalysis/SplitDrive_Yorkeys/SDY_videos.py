import os
import math
import numpy as np
from glob import glob
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import SDY_aux as aux
import SDY_gene as drv
import SDY_land as lnd

# new scripts
import SDY_functions as fun
import SDY_plots as plo

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D


(USR, AOI, THS, QNT) = ('ameek', 'TRS', 0.5, '50')
(DRV, EXP, KEY) = ('SD', 'geo', '01_0001_I')
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
drive = drv.driveSelector(DRV, AOI)
(DVP, NOI) = (drive.get('gDict'), (lnd.ixYK, lnd.ixTP))
colors = drive['colors']
nodes = lnd.IX
# #############################################################################
# Load mean response
# #############################################################################
popFiles = glob(PT_DTA + '*' + KEY + '*')[0]
pts = pd.read_csv(popFiles)
# # #############################################################################
# # Ameek's Scratch Work --> trying to employ mapping
# # #############################################################################
(minLat, minLong) = (min(pts['Latitude']), min(pts['Longitude']))
(maxLat, maxLong) = (max(pts['Latitude']), max(pts['Longitude']))
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
mH = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='h', ax=ax
)
mH.drawcoastlines(color=colors[0], linewidth=2, zorder=1)
mH.drawcoastlines(color=colors[1], linewidth=.25, zorder=2)
mL = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=colors[2], linewidth=10, zorder=0)
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
    list(pts['Longitude']), list(pts['Latitude']), latlon=True,
    alpha=.2, marker='.', s=[10 * math.log(20) for i in list(pts['Longitude'])],
    color='#E048B8', zorder=3
)
fun.quickSaveFig(PT_DTA + 'test.png', fig, dpi=750)
