import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D

pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_Left/LandAggregated"
firstRun = True

for clusterFile in sorted(glob.glob(pathRoot+'/*/Yorkeys*I.csv')):
    clusterstr = clusterFile.split('/')[-2][1:]
    clusterNum  = int(clusterstr) #getfolder name and ignore the C infront of it to chech for the number of clusters

    if clusterNum < 5:
        if firstRun:
            firstRun = False
            #print(clusterFile)
        else:
            break
            #continue
    else:
        break
        #print(clusterFile)

    minLat = 0
    minlong  = 0
    maxLat = 0
    maxLong = 0
    lats = []
    longs = []
    ids = []
    clusterData = open(clusterFile,'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        lat = float(tokens[2])
        long = float(tokens[1])
        id = int(tokens[0])
        lats.append(lat)
        longs.append(long)
        ids.append(id)

    minLat = min(lats)
    minLong  = min(longs)
    maxLat = max(lats)
    maxLong = max(longs)

    fig = plt.figure(figsize=(5, 5))
    ax=fig.add_subplot(111, label="1")
    m = Basemap(projection='merc',llcrnrlat=minLat-0.001,urcrnrlat=maxLat+0.001,llcrnrlon=minLong-0.001,urcrnrlon=maxLong+0.001,lat_ts=20,resolution='i', ax=ax)
    # m.drawcounties(linewidth=0.3)
    # m.drawcoastlines(linewidth=0.3)
    # m.drawcountries(linewidth=0.3)
    m.scatter(longs, lats, latlon=True, alpha=.2, marker='o', s=3)
    tLon,tLat = m(longs,lats)
    for i in range(len(longs)):
        plt.text(tLon[i],tLat[i], ids[i], fontsize=1)
    ax.tick_params(
    axis='both',          # changes apply to the both
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    right=False,
    labelbottom=False, # labels along the bottom edge are off
    labelleft=False)
    plt.savefig(pathRoot+'/images/ids.png', dpi=2048,
                facecolor='w', edgecolor='w', orientation='portrait',
                papertype=None, format="png", transparent=False,
                bbox_inches='tight', pad_inches=0.05, frameon=None)
    plt.close(fig)
    plt.close('all')
