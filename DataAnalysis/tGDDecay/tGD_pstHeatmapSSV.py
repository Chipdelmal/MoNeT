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
# ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']


# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI, MOI) = ('dsk', 'tGD', 'HLT', 'TTS')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (False, True), [.05, .1, .5], True)
(thr, REL_STRT, WRM, ci) = (.05, 1, 0, QNT[1])
(lvls, mthd, xSca, ySca) = (
        [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1],
        'linear', 'linear', 'linear'
    )
# Select surface variables ----------------------------------------------------
(HD_IND, HD_DEP, IND_RAN) = (['ren', 'hnf'], 'ssd', 7)
scalers = (1, 100, 300)
(ngdx, ngdy) = (1000, 1000)
# Spatial settings to sweep through -------------------------------------------
EXPS = ('000', '001', '005', '010', '100')
###############################################################################
# Loop through the experiments
###############################################################################
exp = EXPS[0]
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
monet.makeFolder(PT_IMG)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Heatmap ' + AOI)
###############################################################################
# Analyzes
###############################################################################
# Load files into dataframe
fPtrn = '{}/*{}*{}-{}.csv'.format(PT_OUT, AOI, str(int(ci*100)), MOI)
fName = sorted(glob(fPtrn))
df = pd.read_csv(fName[0])
for filename in fName:
    df = df.append(pd.read_csv(filename))
header = list(df.columns)
headerInd = header[:IND_RAN]
# Filter the dataframe --------------------------------------------------------
# Get the unique values for each indep-var column of the dataframe
uniqueValues = {i: list(df[i].unique()) for i in headerInd}
idTuplesAll = list(product(*uniqueValues.values()))
# Filtering all the experiments of the non-free columns
headFree = [col for col in headerInd if col not in HD_IND]
# Get the unique IDs of the experiments
uniqueIds = [uniqueValues.get(head) for head in headFree]
idTuples = list(product(*uniqueIds))
# Filter the dataframe --------------------------------------------------------
xpId = idTuples[4]
# Loop here
indepFltrs = [list(df[hId[1]] == hId[0]) for hId in zip(xpId, headFree)]
fullFilter = list(map(all, zip(*indepFltrs)))
dfSrf = df[fullFilter]
###############################################################################
# Plot
###############################################################################
# Prepare the response surface ------------------------------------------------
(x, y, z) = (dfSrf[HD_IND[0]], dfSrf[HD_IND[1]], dfSrf[HD_DEP])
(xN, yN, zN) = (
        np.array([float(i/scalers[0]) for i in x]),
        np.array([float(i/scalers[1]) for i in y]),
        np.array([float(i/scalers[2]) for i in z])
    )
(xRan, yRan, zRan) = (aux.axisRange(i) for i in (xN, yN, zN))
(xi, yi) = (
        np.linspace(xRan[0], xRan[1], ngdx),
        np.linspace(yRan[0], yRan[1], ngdy)
    )
zi = griddata((xN, yN), zN, (xi[None, :], yi[:, None]), method=mthd)
# Plot the response surface ---------------------------------------------------
fig, ax = plt.subplots()
ax.plot(xN, yN, 'k.', ms=1, alpha=.25, marker='.')
ax.contour(
        xi, yi, zi, levels=lvls,
        linewidths=.5, colors='k', alpha=.5,
    )
htmp = ax.contourf(
        xi, yi, zi, levels=lvls,
        cmap=aux.cmapB, extend='max'
    )
sz = fig.get_size_inches()[0]
fig.set_size_inches(sz, 1*sz)
