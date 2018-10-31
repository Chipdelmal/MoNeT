# coding: utf-8
################################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Extracts the roads and buildings positions and exports them into
#   SHP and graphml files
# Data source: https://www.openstreetmap.org/
# HMSC, vferman
################################################################################

#Load package ####################################################
import fiona
import numpy as np
import os
import osmnx as ox, geopandas as gpd
import overpy
import sys
ox.config(log_file=True,log_console=True,use_cache=True)


# usage: python buildings.py KM-G 3000

def main():
    #Arguments
    # 0: ISO 3166-2 for the island (e.g. KM-G for grande comore)
    # 1: dintance from lat-long to search for buildings
    clArguments=sys.argv[1:]
    countryCode = clArguments[0]
    distance=int(clArguments[1])
    # Cities and villages ##################################################
    api = overpy.Overpass()
    r = api.query("""
area["ISO3166-2"="KM-G"];
node["place"~"^city$|^village$"](area);
out meta;
""")

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
        size=1000
        try:
            buildings=ox.buildings_from_point(point=locCoord,distance=distance)
            ox.save_gdf_shapefile(buildings,filename=placeName,folder="SHP/Buildings")
            places.append(placeName)
        except KeyError as e:
            print ('error on '+placeName)
        except:
            print ('I got another exception')

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
            placeCoordCSV.write(str(meanLat)+","+str(meanLong)+"\n")
        placeCoordCSV.close()
        placeShapes.close()


main()
