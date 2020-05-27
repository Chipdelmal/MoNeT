#!/usr/bin/python
# -*- coding: utf-8 -*-

import SDY_functions as fun
import compress_pickle as pkl


(VOL, SIG, PRB) = ('RAID5', 'unAggregated', ('Aggregated',))
PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
###############################################################################
# Setting up colors and style
###############################################################################
# Loading the signal files
pth = PATH + 'pre/' + SIG + '/'
sigFiles = fun.getPreProcessedExperiments(pth, 'agg')
# Loading the paths for the probes
prbExpPths = [PATH + 'pre/' + st + '/' for st in PRB]
prbFiles = fun.getPreProcessedExperiments(prbExpPths[0], 'agg')


i = 0

(namS, pthS) = sigFiles[i]
(namP, pthP) = prbFiles[i]
# Load data
dataS = pkl.load(pthS)
dataP = pkl.load(pthP)
(genes, popS) = (dataS['genotypes'], dataS['population'])
(genes, popP) = (dataP['genotypes'], dataP['population'])
err = fun.rpd(popS, popP)

namS

dataP
dataS
