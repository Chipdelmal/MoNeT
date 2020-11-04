
import os
import matplotlib
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
from scipy import stats
import STP_functions as fun
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
import matplotlib.pyplot as plt
from matplotlib import gridspec


(MTR, ERR, OVW, THS, QNT) = ('WOP', False, False, '0.1', '50')
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
    i[0]: da.rescaleDataset(pd.read_csv(i[1]), SCA)
    for i in zip(EXPS, PT_DTA)
}
HEADER = list(dfRC['mixed'].columns)
(LBLS, FEAT_LVLS) = (
    sorted(list(set(HEADER) - set(FEATS))),
    [set(dfRC['mixed'][i].unique()) for i in FEATS]
)
###############################################################################
# Clean the datasets and Export (if needed)
###############################################################################
strErr = 'D'
if ERR:
    strErr = 'E'
strRCDiff = {i: '{}{}_{}_{}'.format(PT_OUT, strErr, i, ID_MTR) for i in EXPS}
dfExist = all([path.isfile(strRCDiff[i]) for i in strRCDiff])
if (not dfExist) or (OVW):
    dfRCDiff = {
        i: da.errorBetweenDataframes(
            dfRC['mixed'], dfRC[i], FEATS, LBLS, error=ERR
        ) 
        for i in dfRC
    }
    ###########################################################################
    # Export datasets
    ###########################################################################
    [dfRCDiff[i].to_csv(strRCDiff[i]) for i in dfRCDiff]
###############################################################################
# Read differences datasets
###############################################################################
if (dfExist) or (not OVW):
    dfRCDiff = {i: pd.read_csv(strRCDiff[i]) for i in EXPS}
###############################################################################
# Analyzes
###############################################################################
data = dfRCDiff['gravidFemale']
data.corr(method='spearman')[THS]
dataNZ = data[THS][data[THS] >= 0]
(fig, ax) = plt.subplots(figsize=(7, 2))
sns.kdeplot(
    dataNZ, 
    fill=True, cut=0, linewidth=1, alpha=.8, zorder=0, common_norm=False
)
# ax.set_xlim(0, 2)
# ax.set_ylim(0, 10)
# Kolmogorov-Smirnov ----------------------------------------------------------
data = (dfRC['mixed'], dfRC['nonGravidFemale'])
dataNZ = [i[THS][i[THS] >= 0] for i in data]
stats.ks_2samp(dataNZ[0], dataNZ[1])
