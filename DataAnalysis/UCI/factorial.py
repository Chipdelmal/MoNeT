#!/usr/bin/python
# -*- coding: utf-8 -*-

import aux
import fun
import numpy as np
import pandas as pd
import MoNeT_MGDrivE as monet
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import scipy.interpolate


(ROOT, LAND, DRIVE_ID, SETTING, THRESHOLDS) = (
        'Volumes', 'Yoosook', 'LDR',
        'island', [.75, .50, .25, .10, .05]
    )
IxOI = [0, ]
PATH_ROOT = '/{}/marshallShare/UCI/{}/{}/'.format(ROOT, LAND, SETTING)

df = pd.read_csv(
        PATH_ROOT + 'thresholdCrosses.csv',
        names=(['key'] + [str(i) for i in THRESHOLDS])
    )

keysStrings = list(df['key'])
keysTuples = [tuple(i.split('_')) for i in keysStrings]
df['key'] = keysTuples

###############################################################################
# Filtering elements of the dataframe
# -----------------------------------------------------------------------------
# fC: Fitness cost
# sV: Standinf variation
# th: Threshold
###############################################################################
(fC, sV, th) = ('100', '0100', '0.5')
filter = [(i[4] == sV) for i in keysTuples]
dfF = df[filter]
# Arrange for plot
(x, y, z) = (
        np.asarray([int(i[1]) / 1000000 for i in dfF['key']]),
        np.asarray([int(i[2]) for i in dfF['key']]),
        np.asarray(list(dfF[th]))
    )

xi, yi = np.linspace(x.min(), x.max(), 1000), np.linspace(y.min(), y.max(), 1000)
xi, yi = np.meshgrid(xi, yi)

rbf = scipy.interpolate.Rbf(x, y, z, function='inverse')
zi = rbf(xi, yi)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
           extent=[x.min(), x.max(), y.min(), y.max()])
ax.set_aspect(.06)
plt.scatter(x, y, c=z)
plt.colorbar()
plt.show()
