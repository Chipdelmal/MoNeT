import numpy as np
import MoNeT_MGDrivE as monet
import vincenty as vn

PLACE = "Fowler"
PATH = "/Volumes/marshallShare/ERACR/Fowler4/Clustered/"
LATLONGS = "fowler_centroids_ordered2.csv"

POI = (-119.690, 36.617)
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')

distances = [vn.vincenty(POI, (row[0], row[1])) for row in latlongs]
inds = np.asarray(distances).argsort()
sortedByDistance = latlongs[inds]
