
import os
import matplotlib
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
import STP_functions as fun
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
import matplotlib.pyplot as plt
from matplotlib import gridspec


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
strRCDiff = {i: '{}{}_{}'.format(PT_OUT, i, ID_MTR) for i in EXPS}
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
    dfRCDiff = {i[0]: pd.read_csv(i[1]) for i in zip(EXPS, strRCDiff)}
###############################################################################
# Analyzes
###############################################################################
data = dfRC['mixed']
data.corr(method='spearman')[THS]
dataNZ = data[THS][data[THS] > 0]
sns.kdeplot(
    dataNZ, 
    fill=True, cut=0, linewidth=1, alpha=.8, zorder=0, common_norm=False
)