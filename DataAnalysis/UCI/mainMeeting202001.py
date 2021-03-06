#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# import aux
import fun
import datetime
import plot
# import argparse
import aux
# import numpy as np
import drive as drv
import matplotlib as mpl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
plt.rcParams.update({'figure.max_open_warning': 0})
mpl.rcParams['axes.linewidth'] = .4


colors = ['#0038a8', '#ff0098', '#ffffff']  # '#9f00cc']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
STYLE_HLT = {
        "width": .175, "alpha": .225, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 3 * 365], "yRange": [0, 525066.0],
        "colors": colors
    }
STYLE_HLT['aspect'] = monet.scaleAspect(.15, STYLE_HLT)


driveID = 'CRISPR'
(thresholds, NOI, SSPOP, REL_STR) = (
        [.5], 0, 10000, 20
    )
style = STYLE_HLT
###############################################################################
# Setting up the experiment analyses
# -----------------------------------------------------------------------------
#   python main.py
#       --dev:  {0: Desktop, 1: Server  }
#       --land:  {0: Comoros, 1: STP     }
###############################################################################
(ROOT, LAND) = ('/Volumes', 'STP')
# Full path ###################################################################
PATH_ROOT = '{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
(PATH_IMG, PATH_DATA) = (PATH_ROOT + 'img/', PATH_ROOT + 'out/')
# Print experiment info to terminal ###########################################
print(aux.PAD)
fun.printExperimentHead(
        PATH_ROOT, PATH_IMG, PATH_DATA,
        str(datetime.datetime.now())
    )
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
(pathTraces, pathMean) = [dir + i for i in ('/GARBAGE/', '/ANALYZED/')]
(dirsTraces, dirsMean) = fun.getTracesAndMeanDirs(pathTraces, pathMean)
# Experiment Selector #########################################################
expOutRootPath = PATH_IMG + driveID
expOutExpPath = expOutRootPath + '/' + fldrName
monet.makeFolder(expOutRootPath)
monet.makeFolder(expOutExpPath)
# for loop here
# Create output folder -------------------------------------------------------
(dirTraces, dirMean) = (dirsTraces[0], dirsMean[0])
expOutSetPath = expOutExpPath + '/' + dirMean.split('/')[-1]
monet.makeFolder(expOutSetPath)
# Mean response --------------------------------------------------------------
filenames = monet.readExperimentFilenames(dirMean)
# Terminal msg
print(aux.PADL)
print('* Loading mean response data...')
landscapeData = monet.loadLandscapeData(filenames, male=True, female=True)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, drvPars.get('HLT')
    )
# Get the max range for each node
maxPops = []
for i in aggregatedNodesData["landscape"]:
    maxPops.append(i[REL_STR][-1] * 1)
# Get the crosses through thresholds
(chngDays, prtcDays, minTuple) = ([], [], [])
for j in range(len(aggregatedNodesData['landscape'])):
    nodePop = aggregatedNodesData['landscape'][j]
    thrsBool = monet.comparePopToThresholds(
            nodePop, gIx, [0, 1], thresholds, refPop=maxPops[j]
        )
    chngDays.append(monet.getConditionChangeDays(thrsBool))
    prtcDays.append(monet.countConditionDays(thrsBool))
    # Get the info to min pop
    nodePopDict = {}
    nodePopDict["population"] = nodePop
    minData = fun.getTimeToMinAtAllele(nodePopDict, gIx, safety=.2)
    minTuple.append(minData)
###############################################################################
# Traces
###############################################################################
paths = monet.listDirectoriesWithPathWithinAPath(dirTraces + '/')
print(
        '* Loading traces reps datasets (' + str(len(paths)) + ') for '
        + ' populations (' + str(len(aggregatedNodesData['landscape']))
        + ')...'
    )
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, drvPars.get('HLT'), male=True, female=True
    )
# Get the max range for each node
maxPops = []
for i in landscapeReps["landscapes"][0]:
    maxPops.append(i[REL_STR][-1] * 1)
# Plot
figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
for j in range(0, len(figsArray)):
    print(
            '* Exporting Population Plots: '
            + '(' + str(j + 1) + '/' + str(len(figsArray)) + ')',
            end='\r'
        )
    # title = plot.parseTitle(thresholds, prtcDays[j])
    title = str(minTuple[j][0]).zfill(4) + " "
    # minTitle = plot.parseMinTitle(minTuple[j], SSPOP, relStr=REL_STR)
    axTemp = figsArray[j].get_axes()[0]
    style['xRange'] = (95, 3 * 365)
    style['yRange'] = (0, maxPops[j] * 1.15)
    style['aspect'] = monet.scaleAspect(.25, style)
    axTemp = plot.setRange(axTemp, style)
    axTemp.set_aspect(aspect=style["aspect"])
    axTemp = plot.removeTicksAndLabels(axTemp)
    axTemp = plot.setAxesColor(axTemp, (0, 0, 0, 0.5))
    expOutStr = expOutSetPath
    figsArray[j].savefig(
            expOutStr + "/Pop_" + str(1 + j).zfill(3) + ".pdf",
            dpi=style['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='pdf',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')
print(
        '* Exporting population plots: '
        + '(' + str(j + 1) + '/' + str(len(figsArray)) + ')...',
        end='\n'
    )
###############################################################################
# Full landscape traces
###############################################################################
print('* Exporting full population traces plot...')
mpl.rcParams['axes.linewidth'] = .2
landscapeRepsFull = monet.sumAggregatedLandscapeDataRepetitionsAlt(
        paths, drvPars.get('HLT'), male=True, female=True
    )
maxPop = landscapeRepsFull['landscapes'][0][0][-1][-1]
figsArray = monet.plotLandscapeDataRepetitions(landscapeRepsFull, style)
# axTemp = plot.printMinTitle(axTemp, str(maxPop/2))
axTemp = figsArray[0].get_axes()[0]
style['xRange'] = (95, 3 * 365)
style['yRange'] = (0, maxPop * 1.1)
style['aspect'] = monet.scaleAspect(.1, style)
axTemp = plot.removeTicksAndLabels(axTemp)
axTemp = plot.setRange(axTemp, style)
axTemp.set_aspect(aspect=style["aspect"])
axTemp = plot.setAxesColor(axTemp, (0, 0, 0, 0.5))
figsArray[0].savefig(
        expOutStr + "/Pop_FULL.pdf", dpi=style['dpi'],
        facecolor=None, edgecolor='w', orientation='portrait', papertype=None,
        format='pdf', transparent=True, bbox_inches='tight',
        pad_inches=.01
    )
plt.close('all')
# Print finished -------------------------------------------------------------
print('* Finished!')
print(aux.PADL)
print(
        aux.CWHT + 'UCI Experiments Analysis '
        + '[' + str(datetime.datetime.now()) + ']' + aux.CEND
    )
print(aux.PAD)
