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

locCoord=(float(clArguments[1]),float(clArguments[2]))

placeName=clArguments[0]
distance=int(clArguments[3])
size=1000
# Buildings ######################################################
buildings=ox.buildings_from_point(point=locCoord,distance=distance)
