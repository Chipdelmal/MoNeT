
import os
import pandas as pd


ID_MTR = 'HLT_WOP_90_qnt.csv'
EXPS = ('mixed', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000

PT_ROT = '/media/hdd/WorkExperiments/STP/PAN/sim/'
PT_DTA = ['{}{}/SUMMARY/{}'.format(PT_ROT, exp, ID_MTR) for exp in EXPS]
DATA = {i[0]: pd.read_csv(i[1]) for i in zip(EXPS, PT_DTA)}

df = DATA['mixed']
HEADER = list(df.columns)
LABELS = set(keys) - set(features)
###############################################################################
# Dataframe cleaning
###############################################################################
df['i_rer'] = df['i_rer'] / SCA
df['i_ren'] = df['i_ren']
df['i_rsg'] = df['i_rsg'] / SCA
df['i_fic'] = df['i_fic'] / SCA
df['i_gsv'] = df['i_gsv'] / SCA
df['i_grp'] = df['i_grp']
[set(df[i].unique()) for i in iKeys]
