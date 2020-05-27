#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import SDY_functions as fun


(VOL, SIG, PRB) = ('RAID5', 'unAggregated', 'Aggregated')
PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
###############################################################################
# Setting up colors and style
###############################################################################
pth = [PATH + 'pre/' + st + '/' for st in (SIG, PRB)]
sigFiles = fun.getPreProcessedExperiments(pth[0], 'sum')

prbFiles = fun.getPreProcessedExperiments(pth[1], 'sum')
