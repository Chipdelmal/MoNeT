#!/usr/bin/python
# -*- coding: utf-8 -*-


###############################################################################
# Video Background Generator
###############################################################################
# import os
import fun
import glob
import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# import numpy as np
from mpl_toolkits.basemap import Basemap
# from mpl_toolkits.mplot3d import Axes3D

PAD = .1
COLORS = [
        fun.rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        fun.rescaleRGBA((255, 0, 152, 255/1)),      # 1: Magenta
        fun.rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        fun.rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        fun.rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        fun.rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]

###############################################################################
pathRoot = '/Volumes/marshallShare/UCI/videoDemo/clustered/'
firstRun = True
###############################################################################
for clusterFile in sorted(glob.glob(pathRoot+'/C*I.csv')):
    clusterstr = clusterFile.split('/')[-1][1:][0:4]
    # getfolder name and ignore the C in front of it to chech for the number
    #   of clusters
    clusterNum = int(clusterstr)

    if clusterNum == 1:
        if firstRun:
            firstRun = False
            print(clusterFile)
        else:
            continue
    else:
        print('*'+clusterFile, end='\r')

    # Read coordinates
    (minLat, maxLat, minLong, maxLong) = (0, 0, 0, 0)
    (lats, longs, clusters, centroidSet) = ([], [], [], {})
    expName = (clusterFile.split("/")[-1]).replace('_I.csv', '_VBG.png')
    clusterData = open(clusterFile, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (lat, long, cluster) = (
                float(tokens[1]), float(tokens[2]), int(tokens[3])
            )
        lats.append(lat)
        longs.append(long)
        clusters.append(cluster)

    (minLat, maxLat, minLong, maxLong) = (
            min(lats), max(lats), min(longs), max(longs)
        )
    (minCluster, maxCluster) = (min(clusters), max(clusters))

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, label="1")
    m = Basemap(
            projection='merc',
            llcrnrlat=minLat-0.025, urcrnrlat=maxLat+0.025,
            llcrnrlon=minLong-0.025, urcrnrlon=maxLong+0.025,
            lat_ts=20, resolution='i', ax=ax
        )
    m.drawcoastlines(color=COLORS[4], linewidth=5, zorder=-1)
    m.drawcoastlines(color=COLORS[0], linewidth=2, zorder=-1)
    m.drawcoastlines(color=COLORS[4], linewidth=.5, zorder=-1)
    # m.fillcontinents(color=COLORS[3], lake_color='aqua')
    m.scatter(
            longs, lats, latlon=True, alpha=.1, marker='x', s=1,
            cmap=plt.get_cmap('winter'), c=clusters,
            vmin=minCluster, vmax=maxCluster
        )
    ax.tick_params(
            axis='both',       # changes apply to the both
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            right=False,
            labelbottom=False,  # labels along the bottom edge are off
            labelleft=False
        )
    ax.axis('off')
    # if not os.path.exists(pathRoot+'/images/C'+clusterstr):
    #     os.mkdir(pathRoot+'/images/C'+clusterstr)
    plt.savefig(pathRoot+'/'+expName, dpi=512,
                facecolor='w', edgecolor='w', orientation='portrait',
                papertype=None, format="png", transparent=False,
                bbox_inches='tight', pad_inches=0.05, frameon=None)
    plt.close(fig)
    plt.close('all')
