#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import statistics as stat
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys4/Experiment4/"
pathSet = pathRoot + "Yorkeys_AGG_*/"  # + "eRACR29"
foldersList = glob.glob(pathSet + "*GARBAGE")
sortedFolders = sorted(foldersList)
sortedFolders


expPath = sortedFolders[2]
gPath = monet.listDirectoriesWithPathWithinAPath(expPath + "/")
ePath = monet.listDirectoriesWithPathWithinAPath(gPath[0] + "/")
aggregationDictionary = monet.autoGenerateGenotypesDictionary(
        ["W", "H", "E", "R", "B"],
        [
            'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
            'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
        ]
    )
reps = monet.loadAndAggregateLandscapeDataRepetitions(
    ePath, aggregationDictionary,
    male=True, female=False
)
repsN = monet.sumAggregatedLandscapeDataRepetitions(reps)
lands = repsN['landscapes']

(geneNumber, totalTime) = (
    len(repsN['genotypes']),
    len(repsN['landscapes'][0][0])
)



(hSD, hMn, hMd) = [np.zeros(shape=(totalTime, geneNumber)) for i in range(3)]
for time in range(totalTime):
    for gene in range(geneNumber):
        slice = [lanRep[0][time, gene] for lanRep in lands]
        (sSD, sMn, sMd) = (stat.stdev(slice), stat.mean(slice), stat.median(slice))
        (hSD[time][gene], hMn[time][gene], hMd[time][gene]) = (sSD, sMn, sMd)
