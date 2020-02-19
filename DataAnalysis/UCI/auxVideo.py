#!/usr/bin/python
# -*- coding: utf-8 -*-

# ############################################################################
# Aux
#   Non-critical functions to help on the analyses
# ############################################################################
import os
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def get_corners(fileName):
    lats = []
    longs = []
    clusterData = open(fileName, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (lat, long) = (float(tokens[1]), float(tokens[2]))
        lats.append(lat)
        longs.append(long)

    minLat = min(lats)
    minLong = min(longs)
    maxLat = max(lats)
    maxLong = max(longs)
    return [[minLong, maxLong], [minLat, maxLat]]


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


def createBasemapInstance(minLat, maxLat, minLon, maxLon, pad=1.5):
    base = Basemap(
            projection='merc',
            lat_0=(maxLat - minLat)/2, lon_0=(maxLon - minLon)/2,
            resolution='h', area_thresh=0.1,
            llcrnrlon=minLon - pad, llcrnrlat=minLat - pad,
            urcrnrlon=maxLon + pad, urcrnrlat=maxLat + pad,
            epsg=4269
        )
    return base


def generateClusterGraphs(
            aggList, coordinates, destination, colorList, original_corners,
            padding, dpi, countries=False, skip=False, refPopSize=1
        ):
    time = len(aggList[0])
    if original_corners:
        fig, ax, m = monet.createFig(original_corners, padding, countries)
    else:
        fig, ax, m = monet.createFig(coordinates, padding, countries)

    for tick in range(time):
        imgFileName = destination+'/c_'+str(tick).zfill(6)+".png"
        if skip and os.path.isfile(imgFileName):
            continue

        for idx, cData in enumerate(aggList):
            pops = []
            try:
                pops = cData[tick]
                alphas, size = monet.getAlphas(pops)
                if alphas:
                    monet.draw_dots(
                            m, alphas, colorList,
                            coordinates[1][idx], coordinates[0][idx],
                            size/refPopSize
                        )
                else:
                    continue
            except Exception as e:
                return e
        else:
            ax.axis('off')
            fig.savefig(imgFileName,
                        dpi=dpi, orientation='portrait', papertype=None,
                        transparent=True, format="png",
                        bbox_inches='tight', pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            if original_corners:
                fig, ax, m = monet.createFig(
                        original_corners, padding, countries
                    )
            else:
                fig, ax, m = monet.createFig(coordinates, padding, countries)

    return
