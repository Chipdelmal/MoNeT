#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import pandas as pd
from glob import glob
import uciPan_drive as drv


USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS, QNT, OVW) = (
        'tParams', 'LDR', 'island', False,
        'HLT', (True, True), [.5, .9, .95], False
    )
header = ['ratio', 'releases', 'fitness', 'sv', 'group']
(thr, REL_STRT, WRM) = (
        [int((1-i) * 100) for i in [.05, .10, .25, .50, .75]],
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

ci = QNT[2]
fNames = sorted(glob('{}*{}.csv'.format(PATH_DATA, str(int(ci*100)))))
raw = pd.read_csv(
        fNames[10], header=None,
        names=header
    )

filter = (raw['group'] == 0) & (raw['sv'] == 1)
raw[filter]
