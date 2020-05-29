#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/23913151/log-log-lmplot-with-seaborn
# https://seaborn.pydata.org/generated/seaborn.heatmap.html

import datetime
import pandas as pd
from glob import glob
import seaborn as sns
import uciPan_drive as drv
import matplotlib.pyplot as plt


USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS, QNT, OVW) = (
        'tParams', 'LDR', 'island', False,
        'HLT', (True, True), [.5, .9, .95], False
    )
header = ['ratio', 'releases', 'fitness', 'sv', 'group']
(thr, REL_STRT, WRM) = (
        [str(int((1-i) * 100)) for i in [.05, .10, .25, .50, .75]],
        1, 0
    )
header.extend(thr)
drvPars = drv.driveSelector(DRV)
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/{}/'.format(LND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/Panmictic/{}/{}/'.format(
        LND, SET)
PATH_DATA = '{}out/LDR/POSTPROCESS/'.format(PATH_ROOT)

ci = QNT[0]

i = 0
fNames = sorted(glob('{}*{}.csv'.format(PATH_DATA, str(int(ci*100)))))
raw = pd.read_csv(fNames[i], header=None, names=header)
filter = (raw['group'] == 0) & (raw['sv'] == 1)
df = raw[filter]

for i in range(1, len(fNames)):
    fNames = sorted(glob('{}*{}.csv'.format(PATH_DATA, str(int(ci*100)))))
    raw = pd.read_csv(fNames[i], header=None, names=header)
    filter = (raw['group'] == 0) & (raw['sv'] == 1)
    df = df.append(raw[filter])

piv = df.pivot('releases', 'ratio', '95')

f, ax = plt.subplots(figsize=(7, 7))
ax.set(xscale="log", yscale="linear")
ax.invert_xaxis()
ax = sns.heatmap(piv, cmap="Blues")
