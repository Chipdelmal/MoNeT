#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import numpy as np
import vincenty as vn
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans

###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS) = (
    "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/",
    "LandscapeOriginal/YorkeysKnob_01_Sort.csv"
)

outFileStr = LATLONGS.split(".")[0].split("/")[1]

###############################################################################
# Matrices calculations
###############################################################################
# Read latlongs
latlongs = np.genfromtxt(
    PATH + LATLONGS, delimiter=',',
    skip_header=1, usecols=[1, 2]
)
# Calculate distance and migration matrices
distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
migrMat = monet.zeroInflatedExponentialMigrationKernel(
    distMat,
    params=monet.AEDES_EXP_PARAMS,
    zeroInflation=pow(lifeStayProb, adultMortality)
)

###############################################################################
# Export files
###############################################################################
