#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
import vincenty as vn
import MoNeT_MGDrivE as monet

###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS) = (
    "/Volumes/marshallShare/SplitDrive_Yorkeys/Landscapes/",
    "LandSorted/Yorkeys01_S.csv"
)
(lifeStayProb, adultMortality) = (.72, .09)

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
outFileStr = LATLONGS.split(".")[0].split("_")[0]
np.savetxt(PATH + outFileStr + "_D.csv", distMat, delimiter=',')
np.savetxt(PATH + outFileStr + "_M.csv", migrMat, delimiter=',')
