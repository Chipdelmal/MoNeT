

import numpy as np
from os import path
import pandas as pd
import seaborn as sns
from scipy import stats
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
import matplotlib.pyplot as plt


(MTR, ERR, OVW, THS, QNT) = ('WOP', False, True, '0.1', '50')
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
EXPS = ('mixed', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000
###############################################################################
# Create directories structure
###############################################################################
PT_ROT = '/media/hdd/WorkExperiments/STP/PAN/sim/'
PT_DTA = ['{}{}/SUMMARY/{}'.format(PT_ROT, exp, ID_MTR) for exp in EXPS]
PT_OUT = PT_ROT + 'SUMMARY/'
PT_IMG = PT_ROT + 'img/'
monet.makeFolder(PT_OUT)
###############################################################################
# Read and clean datasets
###############################################################################
dfRC = {
    i[0]: da.rescaleDataset(pd.read_csv(i[1]), SCA) for i in zip(EXPS, PT_DTA)
}
HEADER = list(dfRC['mixed'].columns)
(LBLS, FEAT_LVLS) = (
    sorted(list(set(HEADER) - set(FEATS))),
    [set(dfRC['mixed'][i].unique()) for i in FEATS]
)
###############################################################################
# Unify Dataframe
###############################################################################
strFull = '{}{}_{}'.format(PT_OUT, 'Full', ID_MTR)
if (not path.isfile(strFull)) or (OVW):
    df = da.unifySexesDataframe(dfRC, EXPS, FEATS, LBLS)
    df.to_csv(strFull)
###############################################################################
# Clean the datasets and Export (if needed)
###############################################################################
strErr = 'D'
if ERR:
    strErr = 'E'
strRCDiff = {i: '{}{}_{}_{}'.format(PT_OUT, strErr, i, ID_MTR) for i in EXPS}
dfExist = all([path.isfile(strRCDiff[i]) for i in strRCDiff])
# Get the difference between sexes composition and baseline -------------------
if (not dfExist) or (OVW):
    dfRCDiff = {
        i: da.errorBetweenDataframes(
            dfRC['mixed'], dfRC[i], FEATS, LBLS, error=ERR
        ) 
        for i in dfRC
    }
    # Export datasets ---------------------------------------------------------
    [dfRCDiff[i].to_csv(strRCDiff[i]) for i in dfRCDiff]
###############################################################################
# Read differences datasets
###############################################################################
if (dfExist) or (not OVW):
    dfRCDiff = {i: pd.read_csv(strRCDiff[i]) for i in EXPS}
###############################################################################
# Analyses
###############################################################################
# Kolmogorov-Smirnov ----------------------------------------------------------
data = (dfRC['gravidFemale'], dfRC['nonGravidFemale'])
filters = [
    [all(f) for f in zip(i[THS] >= 0, i['i_ren'] > 0)] 
    for i in data
]
dataNZ = [i[0][THS][i[1]] for i in zip(data, filters)]
stats.ks_2samp(dataNZ[0], dataNZ[1])
# Quantile --------------------------------------------------------------------
(days, qnt) = (60, .9)
data = dfRCDiff['gravidFemale']
fltr = [all(i) for i in zip(data[THS] >= 0, data['i_ren'] > 0)]
dataNZ = data[THS][fltr]
dataNZSort = sorted(dataNZ)
dataEntries = len(dataNZSort)
tDays = len([i for i in dataNZSort if i < days]) / dataEntries
tQnt = np.quantile(dataNZ, qnt)
(tDays, tQnt)
# Plot ------------------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(7, 2))
sns.kdeplot(
    dataNZ, 
    fill=True, cut=0, linewidth=1, alpha=.8, zorder=0, common_norm=False
)
ax.set_xlim(0, 500)
if ERR:
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 10)
ax.axvline(x=days, zorder=10)
