
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
from sklearn.metrics import plot_confusion_matrix
from sklearn.preprocessing import StandardScaler
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
# Features/Labels Separate ----------------------------------------------------
(modelFeats, classNames) = (
    ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv'],
    ['None', 'Low', 'High']
)
(features, labels) = (dataFiltered[modelFeats], groupIx)
###############################################################################
# Split and preprocess dataset
###############################################################################
(X_train, X_test, y_train, y_test) = train_test_split(
    features, labels, test_size=0.3
)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
###############################################################################
# Train
###############################################################################
rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
[print(i) for i in zip(modelFeats, rf.feature_importances_)]
tree_in_forest = rf.estimators_[0]
tree.plot_tree(
    rf.estimators_[0], filled=True,
    class_names=classNames, feature_names=modelFeats
)
###############################################################################
# Test
###############################################################################
rf.predict(sc.transform([[.1, 1, 0, 0, 0]])) 
plot_confusion_matrix(
    rf, X_test, y_test,
    display_labels=classNames
)
