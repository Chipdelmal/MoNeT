import aux
import MoNeT_MGDrivE as monet
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
# %matplotlib inline

# Setup Paths #################################################################
(BASE_PATH, FILE_COORDS) = (
        '/Volumes/marshallShare/Comoros_STP/Comoros/',
        'all_sites_NEW.csv'
    )
(BASE_PATH, FILE_COORDS) = (
        '/Volumes/marshallShare/Comoros_STP/STP/',
        'stp_all_sites_NEW.csv'
    )
# Setup Style #################################################################
PAD = .1
COLORS = [
        aux.rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        aux.rescaleRGBA((255, 0, 152, 255/1)),      # 1: Magenta
        aux.rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        aux.rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        aux.rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        aux.rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]
# Read LongLats ###############################################################
coordinates = np.genfromtxt(
        BASE_PATH + FILE_COORDS,
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
map.drawcoastlines(color=COLORS[4], linewidth=5, zorder=1)
map.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
map.drawcoastlines(color=COLORS[4], linewidth=.5, zorder=1)
map.fillcontinents(color=COLORS[3], lake_color='aqua')
# map.drawmapboundary(fill_color=COLORS[0])
# map.drawcountries(color=COLORS[0], linewidth=2)
map.scatter(
        [i[0] for i in coordinates], [i[1] for i in coordinates],
        s=.15, alpha=.6, marker='x',
        edgecolors=COLORS[1], color=COLORS[1], zorder=2
    )
plt.savefig(
        BASE_PATH + "Map.png",
        dpi=1000, bbox_inches='tight', pad_inches=0.0, frameon=None
    )
plt.close()