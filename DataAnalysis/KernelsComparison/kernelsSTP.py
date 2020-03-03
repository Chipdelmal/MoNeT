#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import aux
import fun
import datetime
import plot
import numpy as np
import drive as drv
import matplotlib as mpl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
plt.rcParams.update({'figure.max_open_warning': 0})
mpl.rcParams['axes.linewidth'] = .4

driveID = 'LDR'
(thresholds, NOI, SSPOP, REL_STR) = (
        [.1, .25, .5, .75, .9],
        0, 10000, 0
    )
style = aux.STYLE_HLT
###############################################################################
# Setting up the experiment analyses
###############################################################################
# (ROOT, LAND, EXP) = ('Volumes', 'kernels', 'kernel_cluster_10k')
(ROOT, LAND, EXP) = (sys.argv[1], 'kernels', sys.argv[2])
# Full path ------------------------------------------------------------------
PATH_ROOT = '/{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
(PATH_IMG, PATH_DATA) = (PATH_ROOT + 'img/', PATH_ROOT)
dir = '{}{}/'.format(PATH_ROOT, EXP)
# Print experiment info to terminal -------------------------------------------
print(aux.PAD)
fun.printExperimentHead(
        PATH_ROOT, PATH_IMG, dir,
        str(datetime.datetime.now())
    )
###############################################################################
# Selecting drive and get exp dirs
###############################################################################
drvPars = drv.driveSelector(driveID)
gIx = drvPars['HLT']['genotypes'].index('Other')
expSetsDirs = monet.listDirectoriesWithPathWithinAPath(PATH_DATA)
fldrName = dir.split('/')[-1]
(pathTraces, pathMean) = [dir + i for i in ('/GARBAGE/', '/ANALYZED/')]
(dirsTraces, dirsMean) = fun.getTracesAndMeanDirs(pathTraces, pathMean)
# Experiment Selector ---------------------------------------------------------
expOutRootPath = PATH_IMG + driveID
expOutExpPath = expOutRootPath + '/' + fldrName
monet.makeFolder(expOutRootPath)
monet.makeFolder(expOutExpPath)
# Create output folder -------------------------------------------------------
(dirTraces, dirMean) = (dirsTraces[0], dirsMean[0])
expOutSetPath = expOutExpPath + '/' + dirMean.split('/')[-1]
monet.makeFolder(expOutSetPath)
# Mean response --------------------------------------------------------------
filenames = monet.readExperimentFilenames(dirMean)
# Terminal msg ---------------------------------------------------------------
print(aux.PADL)
print('* Loading mean response data...')
# Load mean response and aggregate -------------------------------------------
landscapeData = monet.loadLandscapeData(filenames, male=True, female=True)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, drvPars.get('HLT')
    )
# Get the max range for each node --------------------------------------------
maxPops = []
for i in aggregatedNodesData["landscape"]:
    maxPops.append(i[REL_STR][-1] * 1)
# Get the crosses through thresholds -----------------------------------------
(chngDays, prtcDays, minTuple) = ([], [], [])
for j in range(len(aggregatedNodesData['landscape'])):
    nodePop = aggregatedNodesData['landscape'][j]
    thrsBool = monet.comparePopToThresholds(
            nodePop, gIx, [0, 1], thresholds, refPop=maxPops[j]
        )
    chngDays.append(monet.getConditionChangeDays(thrsBool))
    prtcDays.append(monet.countConditionDays(thrsBool))
    # Get the info to min pop -------------------------------------------------
    nodePopDict = {}
    nodePopDict["population"] = nodePop
    minData = fun.getTimeToMinAtAllele(nodePopDict, gIx, safety=.2)
    minTuple.append(minData)
###############################################################################
# Individual Nodes Traces
###############################################################################
paths = monet.listDirectoriesWithPathWithinAPath(dirTraces + '/')
print(
        '* Loading traces reps datasets (' + str(len(paths)) + ') for ' +
        ' populations (' + str(len(aggregatedNodesData['landscape'])) + ')...'
    )
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, drvPars.get('HLT'), male=True, female=True
    )
# Get the max range for each node ---------------------------------------------
maxPops = []
for i in landscapeReps["landscapes"][0]:
    maxPops.append(i[REL_STR][-1] * 1)
# Plot -----------------------------------------------------------------------
figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
for j in range(0, len(figsArray)):
    print(
            '* Exporting population plots: ({}/{})'.format(
                    str(j + 1), str(len(figsArray))
                ), end='\r'
        )
    title = plot.parseTitle(thresholds, prtcDays[j])
    title = str(minTuple[j][0]).zfill(4) + " "
    axTemp = figsArray[j].get_axes()[0]
    style['yRange'] = (0, maxPops[j] * 1.15)
    style['aspect'] = monet.scaleAspect(.15, style)
    axTemp.set_aspect(aspect=style["aspect"])
    axTemp = plot.setRange(axTemp, style)
    # Add labels to the days of threshold-crossing ----------------------------
    axTemp = plot.printHAxisNumbers(
            axTemp, chngDays[j], style['xRange'][1],
            'Gray', relStr=REL_STR
        )
    axTemp = plot.printVLines(axTemp, chngDays[j])
    # Export to disk ----------------------------------------------------------
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    for spine in axTemp.spines.values():
        spine.set_edgecolor((0, 0, 0, 0.5))
    expOutStr = expOutSetPath
    figsArray[j].savefig(
        expOutStr + "/Pop_" + str(1 + j).zfill(3) + ".pdf", dpi=style['dpi'],
        facecolor=None, edgecolor='w', orientation='portrait', papertype=None,
        format='pdf', transparent=True, bbox_inches='tight',
        pad_inches=.01
    )
    plt.close('all')
print('* Exporting population plots ({})...'.format(len(figsArray)))
###############################################################################
# Full landscape traces
###############################################################################
print('* Exporting full population traces plot...')
mpl.rcParams['axes.linewidth'] = .2
landscapeRepsFull = monet.sumAggregatedLandscapeDataRepetitionsAlt(
        paths, drvPars.get('HLT'), male=True, female=True
    )
land = aggregatedNodesData["landscape"]
summedLand = land[0]
for i in range(1, len(land)):
    summedLand = summedLand + land[i]
maxPop = np.sum(summedLand[-1][-1])
(chngDays, prtcDays, minTuple) = ([], [], [])
thrsBool = monet.comparePopToThresholds(
        summedLand, gIx, [0, 1], thresholds, refPop=maxPop
    )
chngDays.append(monet.getConditionChangeDays(thrsBool))
prtcDays.append(monet.countConditionDays(thrsBool))
# Get the info to min pop ----------------------------------------------------
nodePopDict = {}
nodePopDict["population"] = summedLand
minData = fun.getTimeToMinAtAllele(nodePopDict, gIx, safety=.2)
minTuple.append(minData)
# Plot -----------------------------------------------------------------------
figsArray = monet.plotLandscapeDataRepetitions(landscapeRepsFull, style)
axTemp = figsArray[0].get_axes()[0]
axTemp = plot.printVLines(axTemp, chngDays[0])
axTemp = plot.printHAxisNumbers(
        axTemp, chngDays[0], style['xRange'][1],
        'Gray', relStr=REL_STR
    )
style['yRange'] = (0, maxPop * 1.25)
style['aspect'] = monet.scaleAspect(.15, style)
axTemp = plot.setRange(axTemp, style)
axTemp.set_aspect(aspect=style["aspect"])
axTemp.set_xticks(range(0, style["xRange"][1], 150))
axTemp.tick_params(color=(0, 0, 0, 0.5))
for spine in axTemp.spines.values():
    spine.set_edgecolor((0, 0, 0, 0.5))
figsArray[0].savefig(
    expOutStr + "/Pop_FULL.pdf", dpi=style['dpi'],
    facecolor=None, edgecolor='w', orientation='portrait', papertype=None,
    format='pdf', transparent=True, bbox_inches='tight',
    pad_inches=.01
)
plt.close('all')
###############################################################################
# Goodbye Message
###############################################################################
print('* Finished!')
print(aux.PADL)
print(
        aux.CWHT +
        'UCI Experiments Analysis [{}]'.format(str(datetime.datetime.now())) +
        aux.CEND
    )
print(aux.PAD)
