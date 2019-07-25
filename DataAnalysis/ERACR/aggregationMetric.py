#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import aggregationMetricAux as aux


# ############################################################################
# User-defined experiment input
# ############################################################################
truthExperiment = "Fowler_AGG_1_01500"
pathRoot = "/Volumes/marshallShare/ERACR/Fowler/Experiment/"
# ############################################################################
# Setting up the experiments paths
# ############################################################################
truthExpPath = pathRoot + truthExperiment + "/ANALYZED/*"
pathSet = pathRoot + "Fowler_AGG_1*/"
foldersList = sorted(glob.glob(pathSet + "*ANALYZED"))

# ############################################################################
# Calculating the baseline level (unaggregated)
# ############################################################################
filenames = monet.readExperimentFilenames(glob.glob(truthExpPath)[0] + "/")
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=False, dataType=float
)


landscapeSumData["population"]
