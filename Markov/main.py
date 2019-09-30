# https://ipython-books.github.io/131-simulating-a-discrete-time-markov-chain/

import random
import seaborn as sns
import aux as aux
import bouts as bts
import network as mntw
import landscape as land
import MoNeT_MGDrivE as monet


# ########################################################################
# User-Defined
# ########################################################################
random.seed(1)
(classesNum, mskVct, zeroInflation) = (3, [0, .5, .5], .75)
(lo, hi, ptsNum) = (0, 10, 3)

# ########################################################################
# Mosquito biological behaviour
# ########################################################################
# Create mask matrix: This matrix defines how probable is for a mosquito to
#   move from one life stage to the next (and, as a consequence, from a site
#   type to the next).
mskMat = bts.genMskMat(classesNum, mskVct)
passMkvtest = aux.testMarkovMat(mskMat)
mskMat

# ########################################################################
# Landscape
# ########################################################################
# Creates a random landscape (x,y coordinates) and calculates the distances
#   matrix. Also assigns each coordinate a class. It would make sense to have
#   this in a wrapper function to keep coordinates and classes in the same
#   structure.
landscape = land.genURandLandscape(lo, hi, ptsNum)
distMat = monet.calculateDistanceMatrix(landscape)
sns.heatmap(distMat, annot=True)

# ########################################################################
# Migration
# ########################################################################
migrMat = monet.zeroInflatedExponentialMigrationKernel(
    distMat,
    params=monet.AEDES_EXP_PARAMS,
    zeroInflation=zeroInflation
)
aux.testMarkovMat(migrMat)
sns.heatmap(migrMat, annot=True)

# ########################################################################
# Point types
# ########################################################################
pointClasses = bts.genURandLandscapeClasses(classesNum, ptsNum)
clandMskMat = bts.calcClandMskMat(pointClasses, mskMat)
clandMskMat

# ########################################################################
# Full network
# ########################################################################
network = mntw.normalizeMskMgrMat(migrMat, clandMskMat)
aux.testMarkovMat(network)
sns.heatmap(network, annot=True)

distMat = [[0.0, 540690.9, 6874096, 992515.5, 2917802],[540690.9, 0.0, 7364822, 1102070.6, 2968899], [6874096.0,7364821.8, 0, 7378300.3, 8333337], [992515.5, 1102070.6, 7378300, 0.0, 1928446], [2917802.3, 2968898.7, 8333337, 1928445.8, 0]]
monet.zeroInflatedExponentialMigrationKernel(
    distMat,
    params=monet.AEDES_EXP_PARAMS,
    zeroInflation=zeroInflation
)
