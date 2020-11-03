
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
err = False
(dfDMixed, dfDGravid, dfDNonGravid) = (
    da.errorBetweenDataframes(dfMixed, dfMixed, FEATS, LBLS, error=err),
    da.errorBetweenDataframes(dfMixed, dfGravid, FEATS, LBLS, error=err),
    da.errorBetweenDataframes(dfMixed, dfNonGravid, FEATS, LBLS, error=err)
)
dfMixed.corr()['0.1']
###############################################################################
# Export datasets
###############################################################################
dfDMixed.to_csv('{}{}_{}'.format(PT_OUT, EXPS[0], ID_MTR))
dfDGravid.to_csv('{}{}_{}'.format(PT_OUT, EXPS[1], ID_MTR))
dfDNonGravid.to_csv('{}{}_{}'.format(PT_OUT, EXPS[2], ID_MTR))
###############################################################################
# Plot tests
###############################################################################
# Violin plot -------------------------------------------------------------
THS = '0.1'
(height, jitter, size, alpha) = (.03, .0225, 1, .35)
clrs = ('#ff36b3ff', '#3c47edFF', '#ddf3ffff')
(az, bz, cz) = (
    dfNonGravid[THS][dfNonGravid[THS] > 0],
    dfGravid[THS][dfGravid[THS] > 0],
    dfMixed[THS][dfMixed[THS] > 0]
)
fig = plt.figure(figsize=(7, .75))
spec = gridspec.GridSpec(3, 1, height_ratios=[.5, .5, .5], hspace=0)
ax = []
for i in range(3):
    ax.append(fig.add_subplot(spec[i]))
sns.stripplot(x=az, jitter=jitter, size=size, color=clrs[0], ax=ax[0], alpha=alpha)
sns.stripplot(x=bz, jitter=jitter, size=size, color=clrs[1], ax=ax[1], alpha=alpha)
sns.stripplot(x=cz, jitter=jitter, size=size, color=clrs[2], ax=ax[2], alpha=alpha)
for axt in ax:
    axt.set_ylim(-height, height)
    axt.set_xlim(0, 10 * 365)
    axt.set_yticklabels('')
    axt.set_xticklabels('')
    axt.set_xticks(np.arange(0, 365 * 10, 365))
    axt.set_title('')
    axt.set(xlabel=None)
    [t.set_visible(False) for t in axt.get_yticklines()]
    [t.set_visible(False) for t in axt.get_xticklines()]
    axt.spines['top'].set_visible(False)
    axt.spines['right'].set_visible(False)
    axt.spines['bottom'].set_visible(False)
    axt.spines['left'].set_visible(False)
fun.quickSaveFig(PT_IMG + MTR + '_tResponse.png', fig, transparent=False, dpi=500)
###############################################################################
# Density
###############################################################################
plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (1.0, 1.0, 1.0, 1),  # blue  with alpha = 20%
})
fig = plt.figure(figsize=(7, .75))
gs = gridspec.GridSpec(
    nrows=3, ncols=1, figure=fig, 
    width_ratios= [1], height_ratios=[.5, .5, .5],
    wspace=0.3, hspace=-.85
)
df = (az, bz, cz)
for (i, data) in enumerate(df):
    fig.add_subplot(gs[i, 0])
    ax = sns.kdeplot(data, fill=True, cut=0, color=clrs[i], linewidth=1, alpha=.8, zorder=0, common_norm=False)
    ax = sns.kdeplot(data, fill=False, cut=0, color='#ffffff', linewidth=1.5, alpha=.75, zorder=0, common_norm=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    [t.set_visible(False) for t in ax.get_yticklines()]
    ax.set_yticklabels('')
    ax.set_xticklabels('')
    ax.set_xticks(np.arange(0, 365 * 10, 365))
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title('')
    mxRan = max([max(i) for i in df])
    ax.set_xlim(0, 10 * 365)
plt.show()
fun.quickSaveFig(PT_IMG+'ridge.png', fig, dpi=250, transparent=True)
