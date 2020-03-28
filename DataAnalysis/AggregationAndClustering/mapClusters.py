#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D

pathRoot = "/RAID5/marshallShare/SplitDrive_Yorkeys/Landscapes/LandAggregated/Uniformly/C000100"
firstRun = True

for clusterFile in sorted(glob.glob(pathRoot+'/*/Yorkeys*I.csv')):
    clusterstr = clusterFile.split('/')[-2][1:]
    clusterNum  = int(clusterstr) #getfolder name and ignore the C infront of it to chech for the number of clusters

    if clusterNum == 1:
        if firstRun:
            firstRun = False
            print(clusterFile)
        else:
            continue
    else:
        print(clusterFile)

    (minGroup, maxGroup) = (99999999, 0)
    (minLat, minLong) = (0, 0)
    (maxLat, maxLong) = (0, 0)
    (lats, longs, clusters, centroidSet) = ([], [], [], {})
    expName = (clusterFile.split("/")[-1]).replace('_I.csv', '_VBG_.png')
    clusterData = open(clusterFile, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (lat, long, cluster) = (
                float(tokens[2]), float(tokens[1]), int(tokens[3])
            )
        lats.append(lat)
        longs.append(long)
        clusters.append(cluster)

    (minLat, minLong) = (min(lats), min(longs))
    (minCluster, maxCluster) = (min(clusters), max(clusters))
    (maxLat, maxLong) = (max(lats), max(longs))

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, label="1")
    m = Basemap(
            projection='merc',
            llcrnrlat=minLat-0.001, urcrnrlat=maxLat+0.001,
            llcrnrlon=minLong-0.001, urcrnrlon=maxLong+0.001,
            lat_ts=20, resolution='i', ax=ax
        )
    # m.drawcounties(linewidth=0.3)
    # m.drawcoastlines(linewidth=0.3)
    # m.drawcountries(linewidth=0.3)
    m.scatter(longs, lats, latlon=True, alpha=.2, marker='o', s=3, cmap=plt.get_cmap('rainbow'), c=clusters, vmin=minCluster, vmax=maxCluster)
    # tLon,tLat = m(longs,lats)
    # for i in range(len(longs)):
    #     plt.text(tLon[i],tLat[i], str(i), fontsize=1)
    ax.tick_params(
            axis='both',          # changes apply to the both
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            right=False,
            labelbottom=False, # labels along the bottom edge are off
            labelleft=False
        )
    if not os.path.exists(pathRoot+'/images/C'+clusterstr):
        os.mkdir(pathRoot+'/images/C'+clusterstr)
    plt.savefig(pathRoot+'/images/C'+clusterstr+'/'+expName, dpi=512,
                facecolor='w', edgecolor='w', orientation='portrait',
                papertype=None, format="png", transparent=False,
                bbox_inches='tight', pad_inches=0.05, frameon=None)
    plt.close(fig)
    plt.close('all')
