#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import pandas as pd
import uciPan_fun as fun
# import MoNeT_MGDrivE as monet

(PTH, SMR) = (
        '/home/chipdelmal/Desktop/Panmictic/tParams/',
        'thresholdCrosses.csv'
    )
NMS = ['ratio', 'pattern', 'fit', 'svar', '05', '10', '25', '50', '75']

# Assumes "img" is the first folder!
fldrs = sorted(glob.glob(PTH + "/*/"))[1:]

i = 0
dtaPth = fldrs[i] + SMR
fun.importThresholdsCSV(dtaPth, NMS)
