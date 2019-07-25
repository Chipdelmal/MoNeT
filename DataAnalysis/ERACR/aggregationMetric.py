#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import aggregationMetricAux as aux


truthExperiment = "Fowler_AGG_1_01500"
pathRoot = "/Volumes/marshallShare/ERACR/Fowler/Experiment/"

truthExpPath = pathRoot + truthExperiment + "/"
pathSet = pathRoot + "Fowler_AGG_1*/"
foldersList = sorted(glob.glob(pathSet + "*ANALYZED"))
