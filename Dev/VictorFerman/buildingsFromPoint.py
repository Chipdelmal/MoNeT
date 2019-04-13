import osmnx as ox, geopandas as gpd
import pandas as pd
ox.config(log_file=True,log_console=True,use_cache=True)

def exportBuildingCoordinates(point, name):
    # point must be a tuple (lat,long)
    buildings=ox.buildings_from_point(point=point,distance=5000)
    centroidList = buildings.centroid
    placeCoordCSV = open(name+"_LatLongs.csv","w")
    for i in centroidList:
        placeCoordCSV.write(str(i.y)+','+str(i.x)+'\n')
    placeCoordCSV.close()


exportBuildingCoordinates((35.32, -119.01),'calif')
