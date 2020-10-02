
import os
import numpy as np
import pandas as pd
import STP_dataAnalysis as da


ID_MTR = 'HLT_TTI_90_qnt.csv'
EXPS = ('mixed', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000

PT_ROT = '/media/hdd/WorkExperiments/STP/PAN/sim/'
PT_DTA = ['{}{}/SUMMARY/{}'.format(PT_ROT, exp, ID_MTR) for exp in EXPS]
###############################################################################
# Clean the datasets
###############################################################################
dfAll = (dfMixed, dfGravid, dfNonGravid) = [
    da.rescaleDataset(pd.read_csv(i[1]), SCA) for i in zip(EXPS, PT_DTA)
]
HEADER = list(dfMixed.columns)
LABELS = sorted(list(set(HEADER) - set(FEATS)))
FEAT_LVLS = [set(dfMixed[i].unique()) for i in FEATS]
###############################################################################
# Clean the datasets
###############################################################################
dfDMixed = da.errorBetweenDataframes(dfMixed, dfMixed, FEATS, LABELS)
dfDGravid = da.errorBetweenDataframes(dfMixed, dfGravid, FEATS, LABELS)
dfDNonGravid = da.errorBetweenDataframes(dfMixed, dfNonGravid, FEATS, LABELS)
