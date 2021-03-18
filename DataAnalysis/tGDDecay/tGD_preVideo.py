
import os
import sys
import math
import glob
import numpy as np
import pandas as pd
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from os import path
from glob import glob
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
import PYF_plots as plo
import PYF_functions as fun
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


if monet.isNotebook():
    (USR, DRV, AOI, LND) = ('dsk', 'PGS', 'HLT', 'SPA')
    EXP = 'E_016_024_200_000_000'
else:
    (USR, DRV, AOI, LND, EXP) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
(JOB, TMIN, TMAX) = (8, 1, int(2*365))
EXP_NAM = '{}-{}'.format(EXP, AOI)
###############################################################################
# Setting up paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
PT_VID = path.join(PT_ROT, 'video')
EXP_FLS = sorted(glob(path.join(PT_PRE, EXP_NAM + '*sum.bz')))
EXP_VID = path.join(PT_VID, EXP_NAM)
if len(EXP_FLS) == 0:
    print("Error: No experiment files were found!")
    sys.exit()
monet.makeFolder(PT_VID)
monet.makeFolder(EXP_VID)
# #############################################################################
# Pops counts, coordinates, and aggregations
# #############################################################################
PT_PTS = '/'.join(PT_ROT.split('/')[:-3]) + '/GEO/'
SHPFS = ('bh400kc3500', 'Onetahi')
UA_sites = pd.read_csv(PT_PTS+'Onetahi.csv', sep=',')
UA_sites['pops'] = [int(EXP.split('_')[1])] * UA_sites.shape[0]
GC_RAW = [pkl.load(i)['population'] for i in EXP_FLS]
GC_FRA = [fun.geneCountsToFractions(i) for i in GC_RAW]
DRV_COL = [i[:-2] for i in drv.colorSelector(AOI)]
AG_IDs = lnd.landSelector(LND, '/'.join(PT_PTS.split('/')[:-2]))
# #############################################################################
# Geography
# #############################################################################
# Bounding box ----------------------------------------------------------------
PAD = .00675
point = (-17.0187975, -149.591045)
(minLat, minLong) = [i-PAD for i in point]
(maxLat, maxLong) = [i+PAD for i in point]
# LonLats and populations -----------------------------------------------------
lonLat = UA_sites[['lons', 'lats']]
# Landscape aggregation -------------------------------------------------------
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = fun.aggCentroids(AGG_lonlats)
# #############################################################################
# Checks
# #############################################################################
popsMatch = len(GC_FRA) == len(AGG_lonlats)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_VID, tS, 'PYF PreVideo '+AOI)
# #############################################################################
# Map
# #############################################################################
# Coordinates -----------------------------------------------------------------
(lngs, lats) = (AGG_centroids[:, 0], AGG_centroids[:, 1])
Parallel(n_jobs=JOB)(
    delayed(plo.plotMapFrame)(
        PT_PTS+SHPFS[0],
        time, UA_sites, (minLat, maxLat), (minLong, maxLong), 
        ['#8338EC', '#FF006E', '#0C4887'], GC_FRA, lngs, lats, EXP_VID,
        offset=100, amplitude=150, alpha=.4, marker=(6, 0),
        edgecolor='#F5006A', lw=2
    ) for time in range(TMIN, TMAX))
