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
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import osmnx as ox, geopandas as gpd
import overpy
import sys
ox.config(log_file=True,log_console=True,use_cache=True)


# usage: python buildings.py KM-G 3000
# usage: python buildings.py ST-S 1000

def main():
    #Arguments
    # 0: ISO 3166-2 for the island (e.g. KM-G for grande comore)
    # 1: dintance from lat-long to search for buildings
    clArguments=sys.argv[1:]
    countryCode = clArguments[0]
    distance=int(clArguments[1])
    # Cities and villages ##################################################
    overpassQuery  = 'area["ISO3166-2"="'+countryCode+'"];\n'
    overpassQuery += 'node["place"~"^city$|^village$"](area);\n'
    overpassQuery += 'out meta;'
    api = overpy.Overpass()
    r = api.query(overpassQuery);

    # Buildings ######################################################
    unnamed = 1
    places = []
    for node in r.nodes:
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
                for (lat,long) in coordinateList:
                    lats.append(float(lat))
                    longs.append(float(long))
            meanLat = np.mean(lats)
            meanLong = np.mean(longs)
            fullLats.append(meanLat)
            fullLongs.append(meanLong)
            placeCoordCSV.write(str(meanLat)+","+str(meanLong)+"\n")
        placeCoordCSV.close()
        placeShapes.close()

    minLat = min(fullLats)
    minLong = min(fullLongs)
    maxLat = max(fullLats)
    maxLong = max(fullLongs)

    #fig, ax = plt.subplots()
    m = Basemap(projection='merc',llcrnrlat=minLong-0.03,urcrnrlat=maxLong+0.02,
            llcrnrlon=minLat-0.02,urcrnrlon=maxLat+0.02,lat_ts=20,resolution='h')
    m.drawcoastlines(color="black")

    m.scatter(fullLats,fullLongs,latlon=True,s=9)
    #plt.xlim([minLat+0.02,maxLat+0.02])
    #plt.ylim([minLong+0.02,maxLong+0.02])
    plt.savefig("./"+countryCode+".png", dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches='tight',
                pad_inches=0.05, frameon=None)
    plt.show()
    #plt.close('all')

main()
