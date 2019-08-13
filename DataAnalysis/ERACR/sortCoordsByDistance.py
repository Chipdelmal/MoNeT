import numpy as np
import MoNeT_MGDrivE as monet
import vincenty as vn

PLACE = "Fowler"
PATH = "/Volumes/marshallShare/ERACR/Fowler4/Clustered/"
LATLONGS = "fowler_centroids_ordered2.csv"

POI = (36.617, -119.690)
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')
monet.sortByDistanceToPOI(POI, latlongs, distFun=vn.vincenty)

np.savetxt(
    PATH + "SORTED_TEST_HMSC.csv",
    latlongDistSort,
    fmt='%.10f',
    delimiter=","
)
