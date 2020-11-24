
import os
import math
import glob
import numpy as np
import pandas as pd
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
from os import path
from glob import glob
import SDY_gene as drv
import SDY_land as lnd
import SDY_plots as plo
import SDY_functions as fun
import SDY_dataAnalysis as da


# #############################################################################
# Paths
# #############################################################################
PT_ROT = '/home/chipdelmal/Documents/WorkSims/SDY'
(UA_sites, PT_PRE, PT_VID) = (
    pd.read_csv(path.join(
        PT_ROT,  'Landscapes/LandAggregated/Filtered/C000200/', 
        'Yorkeys01_0010_I.csv'
    )),
    path.join(PT_ROT, 'factorial', 'PREPROCESS/'),
    path.join(PT_ROT, 'factorial', 'video/')
)
EXP_NAM = 'E_1_005_005_10_050-HLT'
EXP_FLS = glob(path.join(PT_PRE, EXP_NAM + '*sum.bz'))
EXP_VID = path.join(PT_VID, EXP_NAM)
monet.makeFolder(PT_VID)
monet.makeFolder(EXP_VID)
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
(BLAT, BLNG) = ((-16.821, -16.80), (145.69, 145.73))
# LonLats and populations -----------------------------------------------------
lonLat = UA_sites[['Lon', 'Lat']]
pop = [20] * lonLat.shape[0]
UA_sites['Pop'] = pop
# Landscape aggregation -------------------------------------------------------
AG_IDs = lnd.VID_IX
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = da.aggCentroids(AGG_lonlats)
# #############################################################################
# Map
# #############################################################################
# Coordinates -----------------------------------------------------------------
(lngs, lats) = (AGG_centroids[:, 0], AGG_centroids[:, 1])
for time in range(GC_FRA[0].shape[0]):
    print('* Exporting {}'.format(str(time).zfill(4)), end='\r')
    # Create map --------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(10, 10))
    (fig, ax, mapR) = plo.plotMap(
        fig, ax, UA_sites, BLAT, BLNG, ptColor='#6347ff'
    )
    # Pops --------------------------------------------------------------------
    (fig, ax, mapR) = plo.plotGenePopsOnMap(
        fig, ax, mapR,
        lngs, lats, DRV_COL, 
        GC_FRA, time, alphaScaler=.5,
        marker=(6, 0), offset=150, amplitude=200, lw=4, ec=(0, 0, 0, .75)
    )
    ax.text(
        0.5, 0.5, str(time).zfill(4), 
        horizontalalignment='center', verticalalignment='center', 
        transform=ax.transAxes, fontsize=30
    )
    fun.quickSaveFig(
        '{}/{}.png'.format(EXP_VID, str(time).zfill(4)),
        fig, dpi=500
    )
    plt.close('all')
