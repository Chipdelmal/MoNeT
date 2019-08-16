#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import MoNeT_MGDrivE as monet
import vincenty as vn
import aux as aux

# Define path, POI, and file
PATH = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/LandscapeOriginal/"
(LATLONGS, POI) = ("YorkeysKnob_01.csv", (-16.83, 145.730))

# Calculate distances to POI and sort
latlongs = np.genfromtxt(PATH + LATLONGS_FILE, delimiter=',')
latlongsSorted = monet.sortByDistanceToPOI(POI, latlongs, distFun=vn.vincenty)
aux.writeLatLongsToFileWithID(
    latlongsSorted, PATH + LATLONGS.split(".")[0] + "_Sort.csv"
)
