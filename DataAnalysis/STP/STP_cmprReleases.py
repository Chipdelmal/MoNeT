
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
dfMixed.corr(method='pearson')['0.1']
###############################################################################
# Export datasets
###############################################################################
dfDMixed.to_csv('{}{}_{}'.format(PT_OUT, EXPS[0], ID_MTR))
dfDGravid.to_csv('{}{}_{}'.format(PT_OUT, EXPS[1], ID_MTR))
dfDNonGravid.to_csv('{}{}_{}'.format(PT_OUT, EXPS[2], ID_MTR))
