#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import STP_land as lnd
import STP_plots as plo
import STP_functions as fun
import STP_gene as drv


plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),
})


PTH_pts = '/media/hdd/WorkExperiments/STP/'
UA_sites = pd.read_csv(PTH_pts+'stp_all_sites_v5.csv')
(lonLat, pop) = (
    UA_sites[['lon', 'lat']], 
    UA_sites['pop']
)
# Landscape aggregation -------------------------------------------------------
AG_IDs = lnd.STP_AGG
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = np.mean(AGG_lonlats, axis=1)
# Drive parameters ------------------------------------------------------------
DRV_COL = [i[:-2] for i in drv.COLHO]
DRV_COL
# Bounding box ----------------------------------------------------------------
(BLAT, BLNG) = ((-0.045, .5), (6.4, 6.8))
# #############################################################################
# Map
# #############################################################################
(fig, ax) = plt.subplots(figsize=(10, 10))
(fig, ax, mL) = plo.plotMap(fig, ax, UA_sites, BLAT, BLNG, ptColor='#6347ff')
# Pops ------------------------------------------------------------------------
(lngs, lats, pops) = (
    AGG_centroids[:, 0], AGG_centroids[:, 1],
    [10000]
)
color = '#ed174b' + ('%02x' % plo.floatToHex(.5))
mL.scatter(
    lngs, lats, 
    latlon=True, marker=(4, 0), 
    s=plo.popsToPtSize(pops, offset=10, amplitude=100),
    c=[color]
)
