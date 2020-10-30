
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


MTR = 'WOP'
ID_MTR = 'HLT_{}_50_qnt.csv'.format(MTR)
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
THS = '0.5'
(height, jitter, size, alpha) = (.03, .0225, 1, .35)
clrs = ('#b8b8ffFF', '#3c47edFF', '#ed174bff')
fig = plt.figure(figsize=(10, 1))
spec = gridspec.GridSpec(3, 1, height_ratios=[.5, .5, .5], hspace=0)
ax = []
for i in range(3):
    ax.append(fig.add_subplot(spec[i]))
sns.stripplot(x=dfNonGravid[THS], jitter=jitter, size=size, color=clrs[0], ax=ax[0], alpha=alpha)
sns.stripplot(x=dfGravid[THS], jitter=jitter, size=size, color=clrs[1], ax=ax[1], alpha=alpha)
sns.stripplot(x=dfMixed[THS], jitter=jitter, size=size, color=clrs[2], ax=ax[2], alpha=alpha)
for axt in ax:
    axt.set_ylim(-height, height)
    axt.set_xlim(0, 6 * 365)
    axt.set_yticklabels('')
    axt.set_xticklabels('')
    axt.set_title('')
    axt.set(xlabel=None)
fun.quickSaveFig(PT_IMG + MTR + '_tResponse.png', fig, transparent=False)


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
fun.quickSaveFig(PT_IMG + MTR + '_tError.png', fig)
###############################################################################
# Density
###############################################################################
fig = plt.figure(figsize=(24, 10))
ax = fig.add_axes([0, 0, 1, 1])
# Violin plot -------------------------------------------------------------
sns.kdeplot(dfNonGravid[THS], fill=False, cut=0, color=clrs[0], linewidth=2.5, alpha=.65, zorder=0, common_norm=False)
sns.kdeplot(dfGravid[THS], fill=False, cut=0, color=clrs[1], linewidth=2.5, alpha=.65, zorder=2, common_norm=False)
sns.kdeplot(dfMixed[THS], fill=False, cut=0, color=clrs[2], linewidth=2.5, alpha=.65, zorder=1, common_norm=False)
sns.kdeplot(dfNonGravid[THS], fill=True, cut=0, color=clrs[0], linewidth=0, alpha=.025, zorder=0, common_norm=False)
sns.kdeplot(dfGravid[THS], fill=True, cut=0, color=clrs[1], linewidth=0, alpha=.025, zorder=2, common_norm=False)
sns.kdeplot(dfMixed[THS], fill=True, cut=0, color=clrs[2], linewidth=0, alpha=.025, zorder=1, common_norm=False)
ax.set_yticklabels('')
ax.set_xticklabels('')
ax.set_title('')
mxRan = max([max(i) for i in (dfNonGravid[THS], dfGravid[THS], dfMixed[THS])])
ax.set_xlim(0, mxRan)
(xrange, yrange) = (ax.get_xlim(), ax.get_ylim())
ax.set_aspect(.25 * (xrange[1]-xrange[0])/(yrange[1]-yrange[0]))
fig.savefig(PT_IMG+'densities.png', dpi=250)
###############################################################################
# Density
###############################################################################
# fig = plt.figure(figsize=(24, 12))
# ax = fig.add_axes([0, 0, 1, 1])
# # Violin plot -------------------------------------------------------------
# sns.kdeplot(dfDNonGravid[THS], fill=True, cut=0, color=clrs[0], linewidth=5, alpha=.25, zorder=0)
# sns.kdeplot(dfDGravid[THS], fill=True, cut=0, color=clrs[1], linewidth=5, alpha=.25, zorder=2)
# sns.kdeplot(dfDMixed[THS], fill=True, cut=0, color=clrs[2], linewidth=5, alpha=.25, zorder=1)
# mxRan = max([max(i) for i in (dfDNonGravid[THS], dfDGravid[THS], dfDMixed[THS])])
# ax.set_xlim(0, mxRan)
# (xrange, yrange) = (ax.get_xlim(), ax.get_ylim())
# ax.set_aspect(.5 * (xrange[1]-xrange[0])/(yrange[1]-yrange[0]))
# fig.savefig(PT_IMG+'densities.png', dpi=500)
