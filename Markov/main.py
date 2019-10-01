# https://ipython-books.github.io/131-simulating-a-discrete-time-markov-chain/

import random
import seaborn as sns
import aux as aux
import bouts as bts
import network as mntw
import landscape as land
import MoNeT_MGDrivE as monet


# ############################################################################
# User-Defined
# ############################################################################
#   zeroInflation: Probability of a mosquito to stay at home
#        (independent of life-stage)
#   lo, hi: Minimum and maximum coordinates for the random points' locations
#   ptsNum: Points number in the environment
# ############################################################################
random.seed(1)
(zeroInflation) = (.75)
(lo, hi, ptsNum) = (0, 10, 6)

# ############################################################################
# Mosquito biological behaviour
# ############################################################################
# mskMat: This matrix defines how probable is for a mosquito to
#   move from one life stage to the next (and, as a consequence, from a site
#   type to the next).
# ############################################################################
mskMat = [
        [0.2, 0.8, 0.0],
        [0.1, 0.7, 0.2],
        [1.0, 0.0, 0.0]
    ]
passMkvtest = aux.testMarkovMat(mskMat)
passMkvtest

# ############################################################################
# Landscape
# ############################################################################
# Creates a random landscape (x,y coordinates) and calculates the distances
#   matrix.
# ############################################################################
landscape = land.genURandLandscape(lo, hi, ptsNum)
distMat = monet.calculateDistanceMatrix(landscape)
sns.heatmap(distMat, annot=True)

# ############################################################################
# Migration
# ############################################################################
# Converts the distances matrix into a proper migration matrix by applying
#   the kernel, and normalizing it.
# ############################################################################
migrMat = monet.zeroInflatedExponentialMigrationKernel(
    distMat,
    params=monet.AEDES_EXP_PARAMS,
    zeroInflation=zeroInflation
)
aux.testMarkovMat(migrMat)
sns.heatmap(migrMat, annot=True)

# ############################################################################
# Point types
# ############################################################################
# Assings classes types to the points in the landscape (this routine will
#   fail if there's few points with respect to the dimension of the point
#   types)
# ############################################################################
pointClasses = bts.genURandLandscapeClasses(len(mskMat), ptsNum)
clandMskMat = bts.calcClandMskMat(pointClasses, mskMat)
clandMskMat
pointClasses

# ############################################################################
# Full network
# ############################################################################
# Applies the point-types mask to the migration matrix, and normalizes it to
#   take into account the movement due to life-stage, and distance.
# ############################################################################
network = mntw.normalizeMskMgrMat(migrMat, clandMskMat)
sns.heatmap(network, annot=True)
aux.testMarkovMat(network)
