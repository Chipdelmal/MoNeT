
import os
import math
import matplotlib
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
from scipy import stats
import plotly.express as px
import STP_functions as fun
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
import matplotlib.pyplot as plt
from matplotlib import gridspec
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.tree import export_graphviz
from sklearn import tree
from dtreeviz.trees import dtreeviz 
from sklearn.ensemble import RandomForestRegressor


(MTR, ERR, OVW, THS, QNT) = ('WOP', False, False, '0.1', '50')
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
EXPS = ('mixed', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000
OPRAN = ((0, 1*365), (1*365, 3*365), (3*365, 100*365))
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
# Preprocess
###############################################################################
# Select dataset and create filter rules --------------------------------------
(dSet, THS) = ('mixed', '0.1')
data = dfRC[dSet]
filterRules = (data[THS] >= 0, data['i_grp'] == 0)
# Filter with rules -----------------------------------------------------------
fltr = [all(i) for i in zip(*filterRules)]
dataFiltered = data[fltr]
dataFiltered.corr(method='spearman')
# sns.pairplot(dataFiltered)
# Calculate Operational Ranges ------------------------------------------------
groupMtr = np.asarray(dataFiltered[THS])
groupBools = [[i[0] <= feat < i[1] for i in OPRAN] for feat in groupMtr]
groupIx = [i.index(True) for i in groupBools]
# kmeans = KMeans(n_clusters=3, random_state=0).fit(kfeats.reshape(-1, 1))
# klabels = kmeans.labels_
###############################################################################
# Cluster
###############################################################################
(features, labels) = (dataFiltered[FEATS], groupIx)
