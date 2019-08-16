#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import FowlerAux as aux
import vincenty as vn
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
from itertools import groupby



seed = 42 # int(time.time())
(lifeStayProb, adultMortality) = (.72, .09)
PATH = "/Volumes/marshallShare/ERACR/Yorkeys4/Clustered/"
(PLACE, LATLONGS) = ("Yorkeys", "YorkeysKnob_01.csv")
