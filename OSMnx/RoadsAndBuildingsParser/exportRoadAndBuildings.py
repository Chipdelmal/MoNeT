################################################################################
# exportRoadAndBuildings.py
# Extracts the roads and buildings positions and exports them into
#   SHP and graphml files
# Data source: https://www.openstreetmap.org/
# HMSC
################################################################################

#Load package ####################################################
import osmnx as ox, geopandas as gpd
import os, sys
#os.chdir('./BRInE/')                           #Uncomment if running from Atom
from IPython.display import Image
ox.config(log_file=True,log_console=True,use_cache=True)
# Define functions ###############################################
def make_plot(place, point, network_type='drive', bldg_color='orange', dpi=250,dist=1000, default_width=4, street_widths=None):
    gdf=ox.buildings_from_point(point=point, distance=dist)
    gdf_proj=ox.project_gdf(gdf)
    fig, ax=ox.plot_figure_ground(point=point, dist=dist, network_type=network_type, default_width=default_width,street_widths=None, save=False, show=False, close=True)
    fig, ax=ox.plot_buildings(gdf_proj, fig=fig, ax=ax, color=bldg_color, set_bounds=False,save=True, show=False, close=True, filename=place, dpi=dpi)
clArguments=sys.argv[1:]
# Location #######################################################

locCoord=(float(clArguments[1]),float(clArguments[2]))          #Comoros

placeName=clArguments[0]
distance=int(clArguments[3])
size=1000
# Buildings ######################################################
buildings=ox.buildings_from_point(point=locCoord,distance=distance)
ox.save_gdf_shapefile(buildings,filename=placeName,folder="SHP/Buildings")
# Roads ##########################################################
roads=ox.graph_from_point(locCoord,distance=distance,network_type='drive')
ox.save_graphml(roads,filename='comoros.graphml',folder="NTW/Roads")
ox.save_graph_shapefile(roads, filename=placeName,folder="SHP/Roads")
# Image ##########################################################
make_plot(placeName,locCoord,dpi=500,dist=distance,default_width=1)
