import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D

pathRoot = "/Volumes/marshallShare/ERACR/Bakersfield/Full"

for clusterFile in glob.glob(pathRoot+'/pusheen*.csv'):
    minGroup = 99999999
    maxGroup = 0
    minLat = 0
    minlong  = 0
    maxLat = 0
    maxLong = 0
    lats = []
    longs = []
    clusters = []
    expName = (clusterFile.split("/")[-1]).replace('csv','png')
    clusterData = open(clusterFile,'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        lat = float(tokens[0])
        long = float(tokens[1])
        cluster = int(tokens[2])
        lats.append(lat)
        longs.append(long)
        clusters.append(cluster)

    minLat = min(lats)
    minLong  = min(longs)
    minCluster = min(clusters)
    maxLat = max(lats)
    maxLong = max(longs)
    maxCluster = max(clusters)

    fig = plt.figure(figsize=(15, 15))
    ax=fig.add_subplot(111, label="1")
    m = Basemap(projection='merc',llcrnrlat=minLat-0.02,urcrnrlat=maxLat+0.02,llcrnrlon=minLong-0.02,urcrnrlon=maxLong+0.02,lat_ts=20,resolution='i', ax=ax)
    m.drawcounties(linewidth=0.3)
    m.scatter(longs, lats, latlon=True, marker='.', s=1, cmap=plt.get_cmap('nipy_spectral'), c=clusters, vmin=minCluster, vmax=maxCluster)
    ax.tick_params(
    axis='both',          # changes apply to the both
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    right=False,
    labelbottom=False, # labels along the bottom edge are off
    labelleft=False)
    plt.savefig(pathRoot+'/'+expName, dpi=2048,
                facecolor='w', edgecolor='w', orientation='portrait',
                papertype=None, format="png", transparent=False,
                bbox_inches='tight', pad_inches=0.05, frameon=None)
    plt.close(fig)
    plt.close('all')
