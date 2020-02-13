#!/usr/bin/python
# -*- coding: utf-8 -*-

# ############################################################################
# Aux
#   Non-critical functions to help on the analyses
# ############################################################################

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
