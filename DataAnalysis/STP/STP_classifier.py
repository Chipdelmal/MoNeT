
import os
import math
import matplotlib
import numpy as np
from os import path
import pandas as pd
from scipy import stats
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
from sklearn import tree
from sklearn import metrics
from dtreeviz.trees import dtreeviz 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


(MTR, ERR, OVW, THS, QNT) = ('WOP', False, False, '0.5', '50')
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
FEATS = ['i_sex', 'i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000
OPRAN = ((0, 1*365), (1*365, 3*365), (3*365, 100*365))
###############################################################################
# Create directories structure
###############################################################################
PT_ROT = '/media/hdd/WorkExperiments/STP/PAN/sim/'
PT_OUT = PT_ROT + 'SUMMARY/'
PT_DTA = '{}{}_{}'.format(PT_OUT, 'Full', ID_MTR)
PT_IMG = PT_ROT + 'img/'
monet.makeFolder(PT_OUT)
###############################################################################
# Read and clean datasets
###############################################################################
dfRC = da.rescaleDataset(pd.read_csv(PT_DTA), SCA)
data = dfRC.drop(dfRC.columns[0], axis=1)
HEADER = list(dfRC.columns)
(LBLS, FEAT_LVLS) = (
    sorted(list(set(HEADER) - set(FEATS))),
    [set(dfRC[i].unique()) for i in FEATS]
)
###############################################################################
# Preprocess
###############################################################################
# Select dataset and create filter rules --------------------------------------
filterRules = (
    data['i_grp'] == 0,
)
# Filter with rules -----------------------------------------------------------
fltr = [all(i) for i in zip(*filterRules)]
dataFiltered = data[fltr]
dataFiltered.corr(method='spearman')[THS]
# sns.pairplot(dataFiltered)
# Calculate Operational Ranges ------------------------------------------------
groupMtr = np.asarray(dataFiltered[THS])
groupBools = [[i[0] <= feat < i[1] for i in OPRAN] for feat in groupMtr]
groupIx = [i.index(True) for i in groupBools]
# kmeans = KMeans(n_clusters=3, random_state=0).fit(kfeats.reshape(-1, 1))
# klabels = kmeans.labels_
###############################################################################
# Split Dataset
###############################################################################
###############################################################################
# Train
###############################################################################
modelFeats = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv']
(features, labels) = (dataFiltered[modelFeats], groupIx)
(X_train, X_test, y_train, y_test) = train_test_split(
    features, labels, test_size=0.3
)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
rf.feature_importances_
