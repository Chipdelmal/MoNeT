#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Clustered video routines
###############################################################################
# In case of:
#   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1
#   https://github.com/matplotlib/basemap/issues/324
#       replace all "utf-8" with "latin-1" in shapefile.py, which located in
#       ~/Library/Python/3.7/lib/python/site-packages/shapefile.py
# Depends on an obsolete structure (needs to be updated):
#   https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/ERACR/Yorkeys.py
#   https://github.com/Chipdelmal/MoNeT/tree/master/DataAnalysis/AggregationAndClustering
# Example of use:
#   python SDY_video.py 'srv' 'agg' 'hlt' 'E_30_30_100'
###############################################################################
import os
import sys
import glob
import warnings
import datetime
import subprocess
import SDY_aux as aux
import SDY_functions as fun
import SDY_select as sel
import MoNeT_MGDrivE as monet
warnings.filterwarnings("ignore", category=UserWarning)

###############################################################################
# Terminal Selections
###############################################################################
# Drive
if sys.argv[1] == 'srv':
    VOL = '/RAID5/marshallShare/'
else:
    VOL = '/home/chipdelmal/Desktop/'
# Landscape
if sys.argv[2] == 'agg':
    (FLD, TYP, CLS) = ('Aggregated', 'Selective', 'C000893')
else:
    (FLD, TYP, CLS) = ('unAggregated', 'Uniformly', 'C002195')
# Health
if sys.argv[3] == 'hlt':
    HLT = True
else:
    HLT = False
###############################################################################
# Paths
###############################################################################
(BASE_PATH, fldName, expName, clstType, kernelName) = (
        '{}SplitDrive_Yorkeys'.format(VOL), 'geoProof',
        FLD, TYP, sys.argv[4]
    )
DATA_PATH = '{}/{}/{}'.format(BASE_PATH, fldName, expName)
(dataFldr, clstFldr, aggLvl, clstSample) = (
        fldName, 'Landscapes/LandAggregated/{}/'.format(clstType),
        CLS, '0001'
    )
(PAD, DPI) = (.001, 512)
###############################################################################
# Colors and genotypes
###############################################################################
(_, aggDict, colors, _) = sel.driveSelectorVideo(1, HLT, '')
###############################################################################
# File paths
###############################################################################
#   BASE_PATH: Root directory for the experiment
#   expFolder: Folder that contains the [ANALYZED, GARBAGE, RAW] sets
#   extras: Folder that contains the [MAP, VBG, CLS, CLL, AGG, AGCV] files
#       generated by the aggregation routines
#   expPath: Folder nested within the ANALYZED folder for parameters sweeps
#       (would be equal to expFolder in case it's not existing)
###############################################################################
(extras, expPath, outPath) = (
        '{}/{}/'.format(BASE_PATH, clstFldr),
        '{}/ANALYZED/{}/'.format(DATA_PATH, kernelName),
        '{}/video/{}/{}/'.format(BASE_PATH, expName, kernelName)
    )
monet.makeFolder(outPath)
###############################################################################
# File names parsing
###############################################################################
#   VBG: Clustered PNG
#   CLL: Number of nodes in cluster?
#   CLS: {x, y, clusterID} -> contained now in "_I"
#   AGG: Aggregated migration matrix "_A"
#   AGCV: Clusters centroids? -> contained now in "_I"
###############################################################################
(patchFilePattern, imagePattern) = (
        {'male': '/M_*', 'female': '/F_*'}, 'c_%06d.png'
    )
(bgName, originalCoordFile) = (
        glob.glob(extras+aggLvl+'/Yorkeys01_'+clstSample+'*_VBG.png')[0],
        glob.glob(extras+aggLvl+'/Yorkeys01_'+clstSample+'*_I.csv')[0]
    )
(imgLocation, videoLocation) = (
        outPath, '{}/video/{}/{}.mp4'.format(BASE_PATH, expName, kernelName)
    )
original_corners = monet.get_corners(originalCoordFile)
(coordinates, clstList) = (
        monet.getClustersFromAggFiles(originalCoordFile),
        monet.readClustersIDs(originalCoordFile)
    )
###############################################################################
# Terminal message
###############################################################################
tStr = datetime.datetime.now()
aux.printVideoHead(BASE_PATH, DATA_PATH, expPath, videoLocation, tStr)
###############################################################################
# Export Frames
###############################################################################
print(aux.CBBL, end='\r')
print('* Populating aggregations list', end='\r')
clusters = monet.populateClustersFromList(clstList, expPath, patchFilePattern)
aggList = monet.aggregateClusters(clusters, aggDict)
# Fixes the sorting of coordinates (add this to the package) ##################
coordinates = (
        [x for _, x in sorted(zip(clstList, coordinates[0]))],
        [x for _, x in sorted(zip(clstList, coordinates[1]))]
    )
# #############################################################################
ticks = aggList[0].shape[0]
fun.generateClusterGraphs(
        originalCoordFile,
        aggList, coordinates, imgLocation, colors, original_corners,
        PAD, DPI, skip=False, countries=False, refPopSize=2
    )
print('* Finished exporting frames ({}/{})'.format(ticks, ticks))
print(aux.CEND, end='\r')
###############################################################################
# Generate video
###############################################################################
console = [
            'ffmpeg', '-y', '-r', '30', '-f', 'image2', '-s', '4096x2160',
            '-i', '{}c_%06d.png'.format(imgLocation),
            '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-vcodec', 'libx264',
            '-crf', '25', '-pix_fmt', 'yuv420p', videoLocation
        ]
FNULL = open(os.devnull, 'w')
video = subprocess.Popen(console, stdout=FNULL, stderr=subprocess.STDOUT)
video.wait()
###############################################################################
# Terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printVideoTail(tStr, tEnd, console, videoLocation)
