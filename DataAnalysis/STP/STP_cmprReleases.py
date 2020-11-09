
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
# Correlation -----------------------------------------------------------------
data = dfRCDiff['gravidFemale']
fltr = [all(i) for i in zip(data[THS] >= 0, data['i_ren'] > 0)]
dataNZ = data[fltr]
dataNZ.corr(method='spearman')[THS]
# Kolmogorov-Smirnov ----------------------------------------------------------
data = (dfRC['mixed'], dfRC['gravidFemale'])
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
###############################################################################
# Clustering
###############################################################################
data = dfRC['mixed']
fltr = [
    all(i) for i in 
    zip(data[THS] >= 0, data['i_ren'] > 0, data['i_gsv'] == 0, data['i_rsg'] == 1.e-05)
]
dataNZ = data[fltr]
X = np.asarray(data[THS])
kmeans = KMeans(n_clusters=3, random_state=0).fit(X.reshape(-1, 1))
kmeans.labels_
# 3D Interactive figure -------------------------------------------------------
s = [(i/(10*365)) for i in dataNZ[THS]]
sz = [(2 + 10 * i/(10*365)) for i in dataNZ[THS]]
fig = go.Figure(data=[go.Scatter3d(
    x=dataNZ['i_fic'], y=dataNZ['i_rer'], z=dataNZ['i_ren'],
    mode='markers',
    marker=dict(
        size=sz,
        color=[(.6, .2, i) for i in s],
        opacity=0.8
    )
)])
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.show()
# Inspect the classes ---------------------------------------------------------
feats = np.asarray(data[THS])
Y = kmeans.labels_
# [i[0] for i in zip(X, labs) if i[1] == 2]
###############################################################################
# Classification
###############################################################################
data = dfRC['mixed']
fltr = [
    all(i) for i in 
    zip(data['i_ren'] > 0)
]
dataNZ = data[fltr]
X = np.asarray(dataNZ[THS])
kmeans = KMeans(n_clusters=3, random_state=0).fit(X.reshape(-1, 1))
iLabels = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv']
(features, labels) = (
    dataNZ[iLabels],
    kmeans.labels_
)
rf = RandomForestRegressor(n_estimators=10, random_state=42)
rf.fit(features, labels)
# _ = tree.plot_tree(rf.estimators_[0], feature_names=iLabels, filled=True)
fig = plt.figure()
ax = fig.gca()
t = dtreeviz(rf.estimators_[0], features, labels, feature_names=iLabels,  fancy=False)
t.save(PT_IMG+'test.svg')
