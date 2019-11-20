import aux
import MoNeT_MGDrivE as monet
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
# %matplotlib inline

BASE_PATH = '/Volumes/marshallShare/Comoros_STP/Comoros/'
PAD = .1
# Setup Style #################################################################
COLORS = [
        aux.rescaleRGBA((47, 28, 191, 255/2.5)), # Faded navy blue
        aux.rescaleRGBA((255, 0, 152, 255/1)),  # Magenta
        aux.rescaleRGBA((37, 216, 17, 255/5)),   # Bright green
        aux.rescaleRGBA((255, 255, 255, 255/1)), # White
        aux.rescaleRGBA((0, 169, 255, 255/10))
    ]
# Read LongLats ###############################################################
coordinates = np.genfromtxt(
        BASE_PATH + 'all_sites_NEW.csv',
        delimiter=',', skip_header=1
    )
# Calculate boundary ##########################################################
(minLon, minLat) = np.amin(coordinates, 0)
(maxLon, maxLat) = np.amax(coordinates, 0)
# Export Map ##################################################################
fig = plt.gcf()
ax = fig.add_subplot(111, label="1")
ax.axis('off')
map = aux.createBasemapInstance(minLat, maxLat, minLon, maxLon, pad=PAD)
# map.arcgisimage(service="NatGeo_World_Map", xpixels=2000)
map.drawcoastlines(color=COLORS[2], linewidth=4, zorder=1)
map.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
map.drawcoastlines(color=COLORS[3], linewidth=.5, zorder=1)
# map.fillcontinents(color=COLORS[4], lake_color='aqua')
# map.drawmapboundary(fill_color=COLORS[4])
# map.drawcountries(color=COLORS[0], linewidth=2)
map.scatter(
        [i[0] for i in coordinates], [i[1] for i in coordinates],
        s=.15, alpha=.75, marker='x',
        edgecolors=COLORS[1], color=COLORS[1], zorder=2
    )
plt.savefig(
        BASE_PATH + "Map_P.png",
        dpi=1000, bbox_inches='tight', pad_inches=0.0, frameon=None
    )
plt.close()
