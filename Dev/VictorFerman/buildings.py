# coding: utf-8
################################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Searches the villages and cities of a country on OSM, then for each it
#  extracts the roads and buildings positions and exports them into
#  SHP and graphml files and finally calculates the centroids of each building
#  and exports the buildings' coordinates to a CSV file
# Data source: https://www.openstreetmap.org/
# HMSC, vferman
################################################################################

#Load package ####################################################
import fiona
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import osmnx as ox, geopandas as gpd
import overpy
import sys
ox.config(log_file=True,log_console=True,use_cache=True)


# usage: python buildings.py KM-G 3000
# usage: python buildings.py ST-S 4000

def querySettlements(countryCode):
    overpassQuery  = 'area["ISO3166-2"="'+countryCode+'"];\n'
    overpassQuery += 'node["place"~"^city$|^village$"](area);\n'
    overpassQuery += 'out meta;'
    api = overpy.Overpass()
    r = api.query(overpassQuery);
    return r

def exportBuildings(settlements,distance):
    unnamed = 1
    places = []
    for node in settlements.nodes:
        locCoord=(float(node.lat),float(node.lon))
        placeName="unnamed"
        if "name:en" in node.tags:
            placeName=node.tags["name:en"]
        elif "name" in node.tags:
            placeName=node.tags["name"]
        else:
            placeName+=str(unnamed)
            unnamed+=1
        try:
            buildings=ox.buildings_from_point(point=locCoord,distance=distance)
            ox.save_gdf_shapefile(buildings,filename=placeName,folder="SHP/Buildings")
            places.append(placeName)
        except KeyError as e:
            print ('error on '+placeName)
        except:
            print ('I got another exception')
    return places

def exportBuildingCoordinates(places):
    fullLats = []
    fullLongs = []
    for place in places:
        filepath = os.path.join(os.getcwd(),"SHP/Buildings/")
        placeShapes = fiona.open(str(filepath)+place+"/"+place+".shp")
        placeCoordCSV = open(str(filepath)+place+"/"+place+"_LatLongs.csv","w")
        for poligon in placeShapes:
            building = poligon['geometry']['coordinates']
            lats = []
            longs = []
            for coordinateList in building:
                for (long,lat) in coordinateList:
                    lats.append(float(lat))
                    longs.append(float(long))
            meanLat = np.mean(lats)
            meanLong = np.mean(longs)
            fullLats.append(meanLat)
            fullLongs.append(meanLong)
            placeCoordCSV.write(str(meanLat)+","+str(meanLong)+"\n")
        placeCoordCSV.close()
        placeShapes.close()
    return (fullLats,fullLongs)

def createGraph(countryCode,fullLats,fullLongs):
    minLat = min(fullLats)
    minLong = min(fullLongs)
    maxLat = max(fullLats)
    maxLong = max(fullLongs)

    m = Basemap(projection='merc',llcrnrlat=minLat-0.03,urcrnrlat=maxLat+0.02,
        llcrnrlon=minLong-0.02,urcrnrlon=maxLong+0.02,lat_ts=20,resolution='h')
    m.drawcoastlines(color="black")
    m.scatter(fullLongs,fullLats,latlon=True,s=9)
    plt.savefig("./"+countryCode+".png", dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches='tight',
                pad_inches=0.05, frameon=None)
    plt.show()

def main():
    #Arguments
    # 0: ISO 3166-2 for the island (e.g. KM-G for grande comore)
    # 1: dintance from lat-long to search for buildings
    clArguments=sys.argv[1:]
    countryCode = clArguments[0]
    distance=int(clArguments[1])
    # Cities and villages ##################################################
    settlements = querySettlements(countryCode)

    # Buildings ######################################################
    places = exportBuildings(settlements,distance)
    (fullLats,fullLongs) = exportBuildingCoordinates(places)

    createGraph(countryCode,fullLats,fullLongs)

main()
