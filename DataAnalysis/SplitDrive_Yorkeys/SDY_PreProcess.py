#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import SDY_ix as sdix
import SDY_aux as aux
import SDY_functions as fun
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
plt.rcParams.update({'figure.max_open_warning': 0})

JOB = 20
(USR, SET) = ('srv', sys.argv[1]) # 'Aggregated')
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
if (SET == 'unAggregated') or (SET == 'Aggregated'):
    if SET == 'Aggregated':
        NOI = sdix.AGGIX
    if SET == 'unAggregated':
        NOI = sdix.NAGIX
else:
    YKR = 891 + 1
    NOI = (list(range(0, YKR)), list(range(YKR, YKR+int(SET[1:]))))
###############################################################################
# Experiment selection parameters
###############################################################################
(MF, SKP, FMT) = ((True, True), False, 'lzma')
DRV = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
# Select form server/desktop
if USR == 'srv':
    PTH_ROOT = '/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/'
else:
    PTH_ROOT = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
# Setup paths and create folders
(PTH_IMG, PTH_DTA, PTH_PRE) = (
        '{}img/{}/'.format(PTH_ROOT, SET),
        '{}{}/'.format(PTH_ROOT, SET),
        '{}pre/{}/'.format(PTH_ROOT, SET),

    )
monet.makeFolders([PTH_IMG, PTH_PRE])
# Print terminal info and create folder
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PTH_DTA, PTH_IMG, PTH_PRE)
###############################################################################
# Setting up paths and directories
###############################################################################
(expDirsMean, expDirsTrac) = fun.getExpPaths(PTH_DTA)
(expNum, nodeDigits) = (len(expDirsMean), 6)
outNames = fun.splitExpNames(PTH_PRE)
expsDone = set(outNames)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
        delayed(fun.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, DRV,
                analysisOI='GEN', prePath=PTH_PRE, nodesAggLst=NOI,
                outExpNames=expsDone, fNameFmt='{}/{}-{}_', OVW=True,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            ) for exIx in range(0, expNum)
    )

# for exIx in range(0, expNum):
#     # Setup paths -------------------------------------------------------------
#     strInt = str(exIx+1).zfill(len(str(expNum)))
#     print('* Analyzing ({}/{})         '.format(strInt, str(expNum)), end='\n')
#     (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx]+'/')
#     expName = pathMean.split('/')[-1]
#     if (expName in expsDone) and (SKP):
#         continue
#     (dirsMean, dirsTraces) = (
#             pathMean, monet.listDirectoriesWithPathWithinAPath(pathTraces)
#         )
#     files = monet.readExperimentFilenames(pathMean)
#     filesList = [monet.filterFilesByIndex(files, ix) for ix in NOI]
#     # Process data
#     print(aux.CBLU + '+ Land repetitions...             ' + aux.CEND, end='\r')
#     landReps = monet.loadAndAggregateLandscapeDataRepetitions(
#             dirsTraces, DRV, MF[0], MF[1]
#         )
#     for (pIx, pop) in enumerate(filesList):
#         fName = '{}/{}-{}_{}'.format(
#                 PTH_PRE, expName, 'GEN', str(pIx).zfill(nodeDigits)
#             )
#         # Load data -----------------------------------------------------------
#         if SUM:
#             print(aux.CBLU + '+ Summed landscape...     ' + aux.CEND, end='\r')
#             sumData = monet.sumLandscapePopulationsFromFiles(pop, MF[0], MF[1])
#             sumAgg = monet.aggregateGenotypesInNode(sumData, DRV)
#             pkl.dump(sumAgg, fName+'_sum'+FMT, compression="lzma")
#         if AGG:
#             print(aux.CBLU + '+ Aggregated landscape... ' + aux.CEND, end='\r')
#             aggData = monet.loadAndAggregateLandscapeData(pop, DRV, MF[0], MF[1])
#             pkl.dump(aggData, fName+'_agg'+FMT, compression="lzma")
#         if SPA:
#             print(aux.CBLU + '+ Spatial landscape...    ' + aux.CEND, end='\r')
#             geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
#             pkl.dump(geneSpaTemp, fName+'_spa'+FMT, compression="lzma")
#         if REP:
#             print(aux.CBLU + '+ Repetitions...          ' + aux.CEND, end='\r')
#             fLandReps = monet.filterAggregateGarbageByIndex(landReps, NOI[pIx])
#             pkl.dump(fLandReps, fName+'_rep'+FMT, compression="lzma")
#         if SRP:
#             print(aux.CBLU + '+ Summed repetitions...   ' + aux.CEND, end='\r')
#             fRepsSum = [sum(i) for i in fLandReps['landscapes']]
#             fRepsDict = {
#                     'genotypes': fLandReps['genotypes'],
#                     'landscapes': fRepsSum
#                 }
#             pkl.dump(fRepsDict, fName+'_srp'+FMT, compression="lzma")
