
# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import glob
import numpy as np
import pandas as pd
import compress_pickle as pkl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os import path
from glob import glob
import STP_gene as drv
import STP_land as lnd
import STP_plots as plo
import STP_functions as fun
import STP_dataAnalysis as da


# #############################################################################
# Paths
# #############################################################################
PT_ROT = '/media/hdd/WorkExperiments/STP/'
(UA_sites, PT_PRE) = (
    pd.read_csv(path.join(PT_ROT, 'stp_all_sites_v5.csv')),
    path.join(PT_ROT, 'PAN', 'sim/mixed/PREPROCESS/')
)
EXP_PAT = 'E_0100000000_04_0000000000_0000000000_0000000000-HLT*sum.bz'
EXP_FLS = glob(path.join(PT_PRE, EXP_PAT))
# #############################################################################
# Pops counts
# #############################################################################
GC_RAW = [pkl.load(i)['population'] for i in EXP_FLS]
GC_FRA = [da.geneCountsToFractions(i) for i in GC_RAW]
DRV_COL = [i[:-2] for i in drv.COLHO]
# #############################################################################
# Geography
# #############################################################################
# Bounding box ----------------------------------------------------------------
(BLAT, BLNG) = ((-0.045, .5), (6.4, 6.8))
# LonLats and populations -----------------------------------------------------
(lonLat, pop) = (UA_sites[['lon', 'lat']], UA_sites['pop'])
# Landscape aggregation -------------------------------------------------------
AG_IDs = lnd.STP_AGG
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = da.aggCentroids(AGG_lonlats)
# #############################################################################
# Checks
# #############################################################################
popsMatch = len(GC_FRA) == len(AGG_lonlats)
# #############################################################################
# Map
# #############################################################################
GC_FRA
# Coordinates -----------------------------------------------------------------
(lngs, lats) = (AGG_centroids[:, 0], AGG_centroids[:, 1])
time = 100
# Create map ------------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(10, 10))
(fig, ax, mapR) = plo.plotMap(fig, ax, UA_sites, BLAT, BLNG, ptColor='#6347ff')
# Pops ------------------------------------------------------------------------
(fig, ax, mapR) = plo.plotGenePopsOnMap(
    fig, ax, mapR,
    lngs, lats, DRV_COL, 
    GC_FRA, time,
    marker=(6, 0), offset=10, amplitude=10
)
ax.text(
    0.4, 0.4, str(time).zfill(4), 
    horizontalalignment='center', verticalalignment='center', 
    transform=ax.transAxes, fontsize=30
)