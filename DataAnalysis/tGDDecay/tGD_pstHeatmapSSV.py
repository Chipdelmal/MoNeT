 #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
from itertools import product
# import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import compress_pickle as pkl
from scipy.interpolate import griddata


# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (False, True), [.05, .1, .5], True)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, True)
(thr, REL_STRT, WRM, ci) = ([.05, .10, .25, .50, .75], 1, 0, QNT[1])
(thrs, lvls, mthd, xSca) = (thr[1], 10, 'nearest', 'log')
EXPS = ('000', '001', '005', '010', '100')
(HD_IND, HD_DEP, IND_RAN) = (['ren', 'frc'], 'ssv', 7)
# ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']
###############################################################################
###############################################################################
exp = EXPS[0]
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
# header = ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']
# header.extend(thr)
monet.makeFolder(PT_IMG)
(ngdx, ngdy) = (1000, 1000)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Heatmap ' + AOI)
###############################################################################
# Analyzes
###############################################################################
# Load files into dataframe
fPtrn = '{}/*{}*{}-TTS.csv'.format(PT_OUT, AOI, str(int(ci*100)))
fName = sorted(glob(fPtrn))
df = pd.read_csv(fName[0])
for filename in fName[1:3]:
    df = df.append(pd.read_csv(filename))
header = list(df.columns)
headerInd = header[:IND_RAN]
# Filter the dataframe --------------------------------------------------------
# Get the unique values for each indep-var column of the dataframe
uniqueValues = {i: list(df[i].unique()) for i in headerInd}
idTuplesAll = list(product(*uniqueValues))
# Filtering all the experiments of the non-free columns
headFree = [col for col in headerInd if col not in HD_IND]
# Get the unique IDs of the experiments
uniqueIds = [uniqueValues.get(head) for head in headFree]
idTuples = list(product(*uniqueIds))
# Filter the dataframe
xpId = idTuples[0]
# Loop here
indepFltrs = [list(df[hId[1]] == hId[0]) for hId in zip(xpId, headFree)]
fullFilter = list(map(all, zip(*indepFltrs)))
df[fullFilter]
