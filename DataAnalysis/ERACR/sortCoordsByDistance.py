import numpy as np
import MoNeT_MGDrivE as monet
import vincenty as vn
import matplotlib.pyplot as plt

PLACE = "Fowler"
PATH = "/Volumes/marshallShare/ERACR/Fowler4/Clustered/"
LATLONGS = "fowler_centroids_ordered2.csv"

POI = (36.617, -119.690)
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')

distances = [vn.vincenty(POI, (row[1], row[0])) for row in latlongs]
inds = np.asarray(distances).argsort()
sortedByDistance = latlongs[inds]

np.savetxt(
    PATH + "SORTED_TEST_HMSC.csv",
    sortedByDistance,
    fmt='%.10f',
    delimiter=","
)

distArray = np.asarray([distances])
latlongDist = np.concatenate((latlongs, distArray.T), axis=1)
latlongDistSort = latlongDist[inds]
np.savetxt(
    PATH + "SORTED_TEST_HMSC.csv",
    latlongDistSort,
    fmt='%.10f',
    delimiter=","
)


plt.figure(figsize=(20, 20))
plt.scatter(
    latlongs[:, 0], latlongs[:, 1], c=distances,
    alpha=.25, cmap='hsv', s=150, linewidth=4
)
plt.tight_layout()
plt.xlim(min(latlongs[:, 0]) - .0005, max(latlongs[:, 0]) + .0005)
plt.ylim(min(latlongs[:, 1]) - .0005, max(latlongs[:, 1]) + .0005)


plt.savefig(
    PATH + PLACE + "_MAP_" + str(CLST_METHOD) + "_" + namePad + ".png",
    dpi=250
)
