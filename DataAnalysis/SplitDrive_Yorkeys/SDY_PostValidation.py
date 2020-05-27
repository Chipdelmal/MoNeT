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
sigFiles = fun.getPreProcessedExperiments(pth, 'sum')

# Loading the paths for the probes
prbExpPths = [PATH + 'pre/' + st + '/' for st in PRB]
prbFiles = fun.getPreProcessedExperiments(prbExpPths[0], 'sum')


i = 0

(namS, pthS) = sigFiles[0]
(namP, pthP) = prbFiles[0]
# Load probe data
data = pkl.load(pthP)
(genes, pop) = (data['genotypes'], data['population'])
fun.rpd(pop, pop)
