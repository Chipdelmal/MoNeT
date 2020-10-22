
import os
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import STP_functions as fun
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
import matplotlib.pyplot as plt
from matplotlib import gridspec


ID_MTR = 'HLT_WOP_90_qnt.csv'
EXPS = ('mixed', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000

PT_ROT = '/media/hdd/WorkExperiments/STP/PAN/sim/'
PT_DTA = ['{}{}/SUMMARY/{}'.format(PT_ROT, exp, ID_MTR) for exp in EXPS]
PT_OUT = PT_ROT + 'SUMMARY/'
monet.makeFolder(PT_OUT)
PT_IMG = PT_ROT + 'img/'
###############################################################################
# Clean the datasets
###############################################################################
dfAll = (dfMixed, dfGravid, dfNonGravid) = [
    da.rescaleDataset(pd.read_csv(i[1]), SCA) for i in zip(EXPS, PT_DTA)
]
HEADER = list(dfMixed.columns)
LBLS = sorted(list(set(HEADER) - set(FEATS)))
FEAT_LVLS = [set(dfMixed[i].unique()) for i in FEATS]
###############################################################################
# Clean the datasets
###############################################################################
err = True
(dfDMixed, dfDGravid, dfDNonGravid) = (
    da.errorBetweenDataframes(dfMixed, dfMixed, FEATS, LBLS, error=err),
    da.errorBetweenDataframes(dfMixed, dfGravid, FEATS, LBLS, error=err),
    da.errorBetweenDataframes(dfMixed, dfNonGravid, FEATS, LBLS, error=err)
)
###############################################################################
# Export datasets
###############################################################################
dfDMixed.to_csv('{}{}_{}'.format(PT_OUT, EXPS[0], ID_MTR))
dfDGravid.to_csv('{}{}_{}'.format(PT_OUT, EXPS[1], ID_MTR))
dfDNonGravid.to_csv('{}{}_{}'.format(PT_OUT, EXPS[2], ID_MTR))
###############################################################################
# Plot tests
###############################################################################
THS = '0.1'
(height, jitter, size) = (.05, .045, .75)
clrs = ('#b8b8ffff', '#d914b5ff', '#04021fff')
fig = plt.figure(figsize=(10, 2.5))
spec = gridspec.GridSpec(3, 1, height_ratios=[.5, .5, .5], hspace=0)
ax = []
for i in range(3):
    ax.append(fig.add_subplot(spec[i]))
sns.stripplot(x=dfNonGravid[THS], jitter=jitter, size=size, color=clrs[0], ax=ax[0])
sns.stripplot(x=dfGravid[THS], jitter=jitter, size=size, color=clrs[1], ax=ax[1])
sns.stripplot(x=dfMixed[THS], jitter=jitter, size=size, color=clrs[2], ax=ax[2])
for axt in ax:
    axt.set_ylim(-height, height)
    axt.set_yticklabels('')
    axt.set_xticklabels('')
    axt.set_title('')
    axt.set(xlabel=None)
fun.quickSaveFig(PT_IMG + 'timeResponse.png', fig)


(height, jitter) = (.05, .04)
fig = plt.figure(figsize=(10, 2.5))
spec = gridspec.GridSpec(3, 1, height_ratios=[.5, .5, .5], hspace=0)
ax = []
for i in range(3):
    ax.append(fig.add_subplot(spec[i]))
sns.stripplot(x=dfDNonGravid[THS], jitter=jitter, size=size, color=clrs[0], ax=ax[0])
sns.stripplot(x=dfDGravid[THS], jitter=jitter, size=size, color=clrs[1], ax=ax[1])
sns.stripplot(x=dfDMixed[THS], jitter=jitter, size=size, color=clrs[2], ax=ax[2])
for axt in ax:
    axt.set_ylim(-height, height)
    axt.set_xlim(-.25, .25)
    axt.set_yticklabels('')
    axt.set_xticklabels('')
    axt.set(xlabel=None)
fun.quickSaveFig(PT_IMG + 'timeError.png', fig)



# fig.savefig(PT_OUT+'test.png', dpi=500)
