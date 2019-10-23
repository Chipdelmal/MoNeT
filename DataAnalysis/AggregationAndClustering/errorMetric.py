#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import statistics as stat
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
###############################################################################
funcsID = ["SSD", "SMN", "SMD"]
funcsList = [stat.stdev, stat.mean, stat.median]
funcsNum = len(funcsList)
###############################################################################

###############################################################################
# Non-Nested Folders Structure
###############################################################################
# pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys4/Experiment4/"
# pathSet = pathRoot + "Yorkeys_AGG_*/"
# foldersList = sorted(glob.glob(pathSet + "*GARBAGE"))
###############################################################################
# for expPath  in foldersList[7:]:
#     # Get paths and aggregate
#     gPath = monet.listDirectoriesWithPathWithinAPath(expPath + "/")
#     ePath = monet.listDirectoriesWithPathWithinAPath(gPath[0] + "/")
#     aggregationDictionary = monet.autoGenerateGenotypesDictionary(
#         ["W", "H", "E", "R", "B"],
#         [
#             'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
#             'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
#         ]
#     )
#     # Landscape calculations
#     # reps = monet.loadAndAggregateLandscapeDataRepetitions(
#     #     ePath, aggregationDictionary, male=True, female=False
#     # )
#     repsN = monet.sumAggregatedLandscapeDataRepetitionsAlt(
#         ePath, aggregationDictionary, male=True, female=False
#     )
#     (genes, lands) = (repsN['genotypes'], repsN['landscapes'])
#     (geneNumber, totalTime) = (len(genes), len(lands[0][0]))
#
#     # Calculate the sumary stats
#     sStats = [np.zeros(shape=(totalTime, geneNumber)) for i in range(funcsNum)]
#     for time in range(totalTime):
#         for gene in range(geneNumber):
#             # Slice the arrays at a certain time for each genotype
#             slice = [lanRep[0][time, gene] for lanRep in lands]
#             sliceStat = [fun(slice) for fun in funcsList]
#             for i in range(funcsNum):
#                 # Add each stat to its corresponding array
#                 sStats[i][time][gene] = sliceStat[i]
#
#     # Export the summary files
#     for i in range(funcsNum):
#         np.savetxt(
#             pathRoot + funcsID[i] + "_" +  expPath.split('/')[-2] + ".csv",
#             sStats[i], fmt='%f', delimiter=',', newline='\n'
#         )

###############################################################################
# Nested Folders Structure
###############################################################################
pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_MINI/Experiemnts/"
pathClst = pathRoot + "C*"
clustersList = sorted(glob.glob(pathClst))
clustersList[9]
###############################################################################
for expPath in [clustersList[9]]:
    sPath = monet.listDirectoriesWithPathWithinAPath(expPath + "/")
    ###########################################################################
    paths = []
    for pth in sPath:
        paths.extend(glob.glob(pth + "/GARBAGE/" + "E*" + "/*"))
    [i + '/' for i in paths]
    ###########################################################################
    aggregationDictionary = monet.autoGenerateGenotypesDictionary(
        ["W", "H", "E", "R", "B"],
        [
            'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
            'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
        ]
    )
    repsN = monet.sumAggregatedLandscapeDataRepetitionsAlt(
        paths, aggregationDictionary, male=True, female=False
    )
    (genes, lands) = (repsN['genotypes'], repsN['landscapes'])
    (geneNumber, totalTime) = (len(genes), len(lands[0][0]))
    # Calculate the sumary stats
    sStats = [np.zeros(shape=(totalTime, geneNumber)) for i in range(funcsNum)]
    for time in range(totalTime):
        for gene in range(geneNumber):
            # Slice the arrays at a certain time for each genotype
            slice = [lanRep[0][time, gene] for lanRep in lands]
            sliceStat = [fun(slice) for fun in funcsList]
            for i in range(funcsNum):
                # Add each stat to its corresponding array
                sStats[i][time][gene] = sliceStat[i]
        # Export the summary files
    for i in range(funcsNum):
        np.savetxt(
            pathRoot + "O_" + expPath.split("/")[-1] + "_" +
                funcsID[i] + ".csv",
            sStats[i], fmt='%f', delimiter=',', newline='\n'
        )
