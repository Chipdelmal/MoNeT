#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Saõ Tomé and Príncipe Kernels Comparisons
#   Use Example: python kernelsSTP.py "Volumes" "kernel_cluster_10k"
###############################################################################

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


(thresholds, SSPOP, MALE, FEMALE) = (
        [.1, .25, .5, .75, .9], 10000, True, True
    )
(xRange, driveID, burn) = (1095, 'LDR', 150)
###############################################################################
# Setting up the experiment analyses
###############################################################################
(ROOT, LAND, EXP) = ('Volumes', 'kernels', 'kernel_cluster_5000')
# (ROOT, LAND, EXP) = (sys.argv[1], 'kernels', sys.argv[2])
# Full path -------------------------------------------------------------------
PATH_ROOT = '/{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
(PATH_IMG, PATH_DATA, dir) = (
        PATH_ROOT + 'img/', PATH_ROOT, '{}{}/'.format(PATH_ROOT, EXP)
    )
# Print experiment info to terminal -------------------------------------------
print(aux.PAD)
fun.printExperimentHead(PATH_ROOT, PATH_IMG, dir, str(datetime.datetime.now()))
###############################################################################
# Selecting drive and get exp dirs
###############################################################################
(REL_STR, style) = (0, aux.STYLE_HLT)
style['xRange'] = (0, xRange)
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
# Create output folder --------------------------------------------------------
(dirTraces, dirMean) = (dirsTraces[0], dirsMean[0])
expOutSetPath = expOutExpPath + '/' + EXP + '/'
monet.makeFolder(expOutSetPath)
# Mean response ---------------------------------------------------------------
print(aux.PADL)
print('* Loading mean response data...')
# Load mean response and aggregate --------------------------------------------
filenames = monet.readExperimentFilenames(dirMean)
landscapeData = monet.loadLandscapeData(filenames, male=MALE, female=FEMALE)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, drvPars.get('HLT')
    )
# Get the max range for each node ---------------------------------------------
maxPops = []
for i in aggregatedNodesData["landscape"]:
    maxPops.append(i[burn][-1] * 1)
# Get the crosses through thresholds ------------------------------------------
(chngDays, prtcDays) = ([], [])
for j in range(len(aggregatedNodesData['landscape'])):
    nodePop = aggregatedNodesData['landscape'][j]
    thrsBool = monet.comparePopToThresholds(
            nodePop, gIx, [0, 1], thresholds, refPop=maxPops[j]
        )
    chngDays.append(monet.getConditionChangeDays(thrsBool))
    prtcDays.append(monet.countConditionDays(thrsBool))
###############################################################################
# Individual Nodes Traces
###############################################################################
paths = monet.listDirectoriesWithPathWithinAPath(dirTraces + '/')
print(
        '* Loading traces reps datasets ({}) for populations ({})...'.format(
                len(paths), len(aggregatedNodesData['landscape'])
            )
    )
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, drvPars.get('HLT'), male=MALE, female=FEMALE
    )
# Get the max range for each node ---------------------------------------------
maxPops = []
for i in landscapeReps["landscapes"][0]:
    maxPops.append(i[burn][-1] * 1)
# Plot ------------------------------------------------------------------------
figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
totalPopsStr = str(len(figsArray)).zfill(3)
for j in range(0, len(figsArray)):
    print(
            '* Exporting population plots ({}/{})...'.format(
                    str(j+1).zfill(3), totalPopsStr
                ), end='\r'
        )
    axTemp = figsArray[j].get_axes()[0]
    style['yRange'] = (0, maxPops[j] * 1.15)
    style['aspect'] = monet.scaleAspect(.15, style)
    axTemp.set_aspect(aspect=style["aspect"])
    axTemp = plot.setRange(axTemp, style)
    # Add labels to the days of threshold-crossing ----------------------------
    axTemp = plot.printHAxisNumbers(
            axTemp, chngDays[j], style['xRange'][1], 'Gray', relStr=REL_STR
        )
    axTemp = plot.printVLines(axTemp, chngDays[j])
    # Export to disk ----------------------------------------------------------
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    for spine in axTemp.spines.values():
        spine.set_edgecolor((0, 0, 0, 0.5))
    expOutStr = expOutSetPath
    figsArray[j].savefig(
        expOutStr + "/Pop_" + str(1+j).zfill(3) + ".pdf", dpi=style['dpi'],
        facecolor=None, edgecolor='w', orientation='portrait', papertype=None,
        format='pdf', transparent=True, bbox_inches='tight',
        pad_inches=.01
    )
    plt.close('all')
print(
        '* Exporting population plots ({}/{})...'.format(
                totalPopsStr, totalPopsStr
            )
    )
###############################################################################
# Heatmap
###############################################################################
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)
geneSpatiotemporals_normalized = monet.rescaleGeneSpatiotemporals(
        geneSpatiotemporals
    )
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals_normalized,
    style={"aspect": .25, "cmap": aux.cmapsS},
    vmax=1
)
overlay.savefig(
    expOutSetPath + "/Heatmap.pdf", dpi=style['dpi'],
    facecolor=None, edgecolor='w', orientation='portrait', papertype=None,
    format='pdf', transparent=True, bbox_inches='tight',
    pad_inches=.01
)
plt.close()
###############################################################################
# Full landscape traces
###############################################################################
print('* Exporting full population traces plot...')
mpl.rcParams['axes.linewidth'] = .2
# Load landscape traces as a full set -----------------------------------------
landscapeRepsFull = monet.sumAggregatedLandscapeDataRepetitionsAlt(
        paths, drvPars.get('HLT'), male=MALE, female=FEMALE
    )
# Sum mean landscape into one node --------------------------------------------
land = aggregatedNodesData["landscape"]
summedLand = land[0]
for i in range(1, len(land)):
    summedLand = summedLand + land[i]
maxPop = np.sum(summedLand[-1][-1])
(chngDays, prtcDays) = ([], [])
thrsBool = monet.comparePopToThresholds(
        summedLand, gIx, [0, 1], thresholds, refPop=maxPop
    )
chngDays.append(monet.getConditionChangeDays(thrsBool))
prtcDays.append(monet.countConditionDays(thrsBool))
# Plot ------------------------------------------------------------------------
figsArray = monet.plotLandscapeDataRepetitions(landscapeRepsFull, style)
axTemp = figsArray[0].get_axes()[0]
axTemp = plot.printVLines(axTemp, chngDays[0])
axTemp = plot.printHAxisNumbers(
        axTemp, chngDays[0], style['xRange'][1], 'Gray', relStr=REL_STR
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
