#!/usr/bin/python
# -*- coding: utf-8 -*-

import uciPan_fun as fun
# import MoNeT_MGDrivE as monet

(PTH, SMR) = (
        '/home/chipdelmal/Desktop/Panmictic/tParams/',
        'thresholdCrosses.csv'
    )

# Setup dataframe's column names
(THS, NMS, SCH) = (
        ['05', '10', '25', '50', '75'],
        ['ratio', 'pattern', 'fit', 'svar'],
        ['island', 'islandGravidFemales', 'islandMixed']
    )
names = fun.ammendHeader(NMS, THS)

# Iterate through folders (island, mixed, gravid)
for schm in SCH:
    dtaPth = PTH+schm+'/'
    xpDF = fun.importThresholdsCSV(dtaPth+SMR, NMS)
    # Unique values for each input tuple
    (rV, pV, fV, sV) = [list(xpDF[i].unique()) for i in names[0:4]]

    for sVFltr in sV:
        filter = xpDF['svar'] == sVFltr
        ftDF = xpDF[filter][['ratio', 'pattern', 'W50', 'W10']]
        ftDF.to_csv(dtaPth+'SV_'+sVFltr+'.csv', index=False)
