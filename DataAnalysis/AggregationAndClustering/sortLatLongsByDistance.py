#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import MoNeT_MGDrivE as monet
import vincenty as vn
import aux as aux

###############################################################################
# Parameters Setup
###############################################################################
PATH = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/"
(LATLONGS, OUT_FOLDER, POI) = (
    "LandOriginal/Yorkeys03.csv",
    "LandSorted/",
    (-16.83, 145.730)
)

###############################################################################
# POI Operations
###############################################################################
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')
latlongsSorted = monet.sortByDistanceToPOI(POI, latlongs, distFun=vn.vincenty)

###############################################################################
# Export files
###############################################################################
aux.writeLatLongsToFileWithID(
    latlongsSorted,
    PATH + OUT_FOLDER + LATLONGS.split(".")[0].split("/")[1] + "_S.csv"
)
