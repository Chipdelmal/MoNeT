#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# import aux
import fun
import datetime
import argparse
import aux
import drive as drv
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet


driveID = 'CRISPR'
(thresholds, NOI, SSPOP, REL_STR) = (
        [.95, .9, .75, .5, .25, .1, .05],
        0, 10000, 20
    )
style = aux.STYLE_HLT
###############################################################################
# Setting up the experiment analyses
# -----------------------------------------------------------------------------
#   python main.py
#       --dev:  {0: Desktop, 1: Server  }
#       --land:  {0: Comoros, 1: STP     }
###############################################################################
# parser = argparse.ArgumentParser(description='Main UCI Analysis routine!')
# parser.add_argument("--dev", default=0, type=int, help="Device")
# parser.add_argument("--land", default=0, type=int, help="Landscape")
# (ROOT, LAND) = fun.experimentSelector(parser.parse_args())
(ROOT, LAND) = ('/Volumes', 'Comoros')
# Full path ###################################################################
PATH_ROOT = '{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
(PATH_IMG, PATH_DATA) = (PATH_ROOT + 'img/', PATH_ROOT + 'out/')
# Print experiment info to terminal ###########################################
time = str(datetime.datetime.now())
fun.printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time)

###############################################################################
# Selecting drive and get exp dirs
# -----------------------------------------------------------------------------
###############################################################################
drvPars = drv.driveSelector(driveID)
gIx = drvPars['HLT']['genotypes'].index('Other')
expSetsDirs = monet.listDirectoriesWithPathWithinAPath(PATH_DATA)
# Kernel Selector #############################################################
dir = expSetsDirs[0]
# for loop here
fldrName = dir.split('/')[-1]
(pathTraces, pathMean) = (dir + '/GARBAGE/', dir + '/ANALYZED/')
(dirsTraces, dirsMean) = (
        monet.listDirectoriesWithPathWithinAPath(pathTraces),
        monet.listDirectoriesWithPathWithinAPath(pathMean)
    )
# Experiment Selector #########################################################
expOutRootPath = PATH_IMG + driveID
monet.makeFolder(expOutRootPath)
expOutExpPath = expOutRootPath + '/' + fldrName
monet.makeFolder(expOutExpPath)
# for loop here
# Create output folder -------------------------------------------------------
(dirTraces, dirMean) = (dirsTraces[0], dirsMean[0])
expOutSetPath = expOutExpPath + '/' + dirMean.split('/')[-1]
monet.makeFolder(expOutSetPath)
# Mean response --------------------------------------------------------------
filenames = monet.readExperimentFilenames(dirMean)
landscapeData = monet.loadLandscapeData(filenames, male=True, female=True)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, drvPars.get('HLT')
    )
# Get the crosses through thresholds
(chngDays, prtcDays, minTuple) = ([], [], [])
for j in range(len(aggregatedNodesData['landscape'])):
    nodePop = aggregatedNodesData['landscape'][j]
    thrsBool = monet.comparePopToThresholds(
            nodePop, gIx, [0, 1], thresholds, refPop=SSPOP
        )
    chngDays.append(monet.getConditionChangeDays(thrsBool))
    prtcDays.append(monet.countConditionDays(thrsBool))
    # Get the info to min pop
    nodePopDict = {}
    nodePopDict["population"] = nodePop
    minData = fun.getTimeToMinAtAllele(nodePopDict, gIx)
    minTuple.append(minData)
# Traces ---------------------------------------------------------------------
paths = monet.listDirectoriesWithPathWithinAPath(dirTraces + '/')
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, drvPars.get('HLT'), male=True, female=True
    )
# Plot
figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
for j in range(0, len(figsArray)):
    title = fun.parseTitle(thresholds, prtcDays[j])
    minTitle = fun.parseMinTitle(minTuple[j], SSPOP, relStr=REL_STR)
    axTemp = figsArray[j].get_axes()[0]
    axTemp = fun.setRange(axTemp, style)
    # Add labels to the days of threshold-crossing
    axTemp = fun.printHAxisNumbersAlt(
            axTemp, chngDays[j], style['xRange'][1], 'Gray',
            relStr=REL_STR
        )
    # Min pop prints
    if(1 - minTuple[j][1] / SSPOP >= .05):
        axTemp = fun.printHAxisNumbers(
                axTemp, [minTuple[j][0]], style['xRange'][1], 'Red',
                top=False, relStr=REL_STR
            )
        axTemp = fun.printVAxisNumbers(
                axTemp, [minTuple[j][1] / SSPOP],
                style['yRange'][1], 'Red', left=True, rnd=False
            )
        axTemp = fun.printMinLines(
                axTemp, (minTuple[j][0], minTuple[j][1] / SSPOP),
                style, SSPOP
            )
    # Titles and lines common for both analyses
    axTemp = fun.printTitle(axTemp, title)
    axTemp = fun.printMinTitle(axTemp, minTitle)
    axTemp = fun.printVLines(axTemp, chngDays[j])
    # Export to disk
    expOutStr = expOutSetPath
    monet.quickSaveFigure(
            figsArray[j], expOutStr + "_N" + str(j) + ".pdf",
            dpi=style['dpi'], format='pdf'
        )
plt.close('all')
