import osmnx as ox, geopandas as gpd
import pandas as pd
ox.config(log_file=True,log_console=True,use_cache=True)

def exportBuildingCoordinates(point, name):
    # point must be a tuple (lat,long)
    buildings=ox.buildings_from_point(point=point,distance=1800)
    centroidList = buildings.centroid
    placeCoordCSV = open(name+"_LatLongs.csv","w")
    for i in centroidList:
        placeCoordCSV.write(str(i.y)+','+str(i.x)+'\n')
    placeCoordCSV.close()
    network = ox.graph_from_point(point,distance=1800)
    ox.save_graphml(network,filename=name+'.grpahml',folder='network')
    ox.save_graph_shapefile(network, filename=name,folder='network')


exportBuildingCoordinates((35.3532, -119.1148),'barkersfiel3')
