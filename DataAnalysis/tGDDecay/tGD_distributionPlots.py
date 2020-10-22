#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import warnings
import tGD_aux as aux
import tGD_fun as fun
import numpy as np
from itertools import product
from datetime import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings("ignore")
# ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']


# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(FMT, SKP, MF, OVW, QNT) = ('bz', False, (False, True), True, '50')
# Select surface variables ----------------------------------------------------
HD_IND = ['i_ren', 'i_hnf']
(ngdx, ngdy) = (1000, 1000)
(lvls, mthd, xSca, ySca) = (
        [-.05, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.05],
        'linear', 'linear', 'linear'
    )
(exp, moi, mtr) = ('000', 'WOP', '0.1')
(scalers, HD_DEP, _, cmapR) = aux.selectDepVars(moi, float(mtr), AOI)
cmap = cmapR.reversed()
###########################################################################
# Loop through the experiments
###########################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_IMG = PT_IMG + 'violin/'
monet.makeFolder(PT_IMG)
PT_IMG = PT_IMG+'-'.join(HD_IND)+'/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_MTR, tS, 'Violin '+AOI)
#######################################################################
# Analyzes
#######################################################################
# Load files into dataframe
fPtrn = '{}{}_{}_{}_qnt.csv'.format(PT_MTR, AOI, moi, QNT)
(df, header, headerInd) = aux.loadDFFromSummary(fPtrn)
# (fig, ax) = plt.subplots()
# ax = sns.violinplot(
#     x=mtr, y='i_ren', data=df, palette="muted", cut=0, split=False, orient='h',
#     ax=ax
# )
(fig, ax) = plt.subplots()
HNF = list(set(df['i_hnf']))
colors = plt.cm.RdPu(np.linspace(0, 1, 100))
for (i, hnf) in enumerate(HNF):
    fltrPairs = (list(df['i_hnf'] == hnf), list(df['i_ren'] >= 1))
    fltr = list(map(all, zip(*fltrPairs)))
    plt.plot(
        list(df['i_ren'][fltr]), list(df['0.5'][fltr]),
        color=colors[i]
    )
fig = fun.quickSaveFig(PT_IMG + 'WOP.png', fig)


(exp, moi, mtr) = ('000', 'MNX', '0.1')
(scalers, HD_DEP, _, cmapR) = aux.selectDepVars(moi, float(mtr), AOI)
cmap = cmapR.reversed()
###########################################################################
# Loop through the experiments
###########################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_IMG = PT_IMG + 'violin/'
monet.makeFolder(PT_IMG)
PT_IMG = PT_IMG+'-'.join(HD_IND)+'/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_MTR, tS, 'Violin '+AOI)
#######################################################################
# Analyzes
#######################################################################
# Load files into dataframe
fPtrn = '{}{}_{}_{}_qnt.csv'.format(PT_MTR, AOI, moi, QNT)
(df, header, headerInd) = aux.loadDFFromSummary(fPtrn)
(fig, ax) = plt.subplots()
HNF = list(set(df['i_hnf']))
for hnf in HNF[:]:
    fltrPairs = (list(df['i_hnf'] == hnf), list(df['i_ren'] >= 1))
    fltr = list(map(all, zip(*fltrPairs)))
    plt.plot(
        list(df['i_ren'][fltr]), list(df['min'][fltr]), cmap='RdPu'
    )
fig = fun.quickSaveFig(PT_IMG + 'MNX.png', fig)
