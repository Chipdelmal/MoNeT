#!/usr/bin/python
# -*- coding: utf-8 -*-

# ############################################################################
# Aux
#   Non-critical functions to help on the analyses
# ############################################################################

from mpl_toolkits.basemap import Basemap


def listColumnsNumbers(data):
    return ["{}. {}".format(i, col) for (i, col) in enumerate(list(data.columns))]


def printList(listIn):
    [print(i) for i in listColumnsNumbers(listIn)]
    return True


def printFormattedList(dataList):
    [print("* **" + i + "**: ") for i in listColumnsNumbers(dataList)]
    return True


def getYearFromCol(dataCol):
    return [i.year for i in dataCol]


def getNumericalRange(dataCol):
    rangeTuple = (min(dataCol), max(dataCol))
    return rangeTuple


def stringCategorySet(dataCol):
    catSet = [str(i) for i in set(dataCol)]
    return ', '.join(catSet)


def getCoordsMinMaxes(coordColumn):
    (minLat, maxLat) = (
        min(coordColumn),
        max(coordColumn)
    )
    return (minLat, maxLat)


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


def createBasemapInstance(minLat, maxLat, minLon, maxLon, pad=1.5):
    base = Basemap(projection='merc',
        lat_0=(maxLat - minLat)/2, lon_0=(maxLon - minLon)/2,
        resolution='h', area_thresh=0.1,
        llcrnrlon=minLon - pad, llcrnrlat=minLat - pad,
        urcrnrlon=maxLon + pad, urcrnrlat=maxLat + pad,
        epsg=4269
    )
    return base
