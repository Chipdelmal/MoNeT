import random
import seaborn as sns
import aux as aux
import bouts as bts
import network as mntw
import landscape as land
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

zeroInflation = 0.5
landscapeProb = [0.7, 0.2, 0.1]
n = 100
def genSingle(n, zeroInflation, landscapeProb):
    (lo, hi, n) = (0, 10, n)
    # ############################################################################
    # Mosquito biological behaviour
    # ############################################################################
    # mskMat: This matrix defines how probable is for a mosquito to
    #   move from one life stage to the next (and, as a consequence, from a site
    #   type to the next).
    # ############################################################################
    mskMat = [
            [0.20, 0.80, 0.00],
            [0.10, 0.75, 0.15],
            [0.80, 0.00, 0.20]
        ]
    passMkvtest = aux.testMarkovMat(mskMat)
    passMkvtest
    # ############################################################################
    # Landscape
    # ############################################################################
    # Creates a random landscape (x,y coordinates) and calculates the distances
    #   matrix.
    # ############################################################################
    landscape = land.genUniformLandscape(lo, hi, n)
    distMat = monet.calculateDistanceMatrix(landscape)

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

    # ############################################################################
    # Point types
    # ############################################################################
    # Assigns classes types to the points in the landscape (this routine will
    #   fail if there's few points with respect to the dimension of the point
    #   types)
    # ############################################################################
    #pointClasses = bts.genURandLandscapeClasses(len(mskMat), n)

    pointClasses = bts.genMRandLanscapeClasses(len(mskMat), n, landscapeProb)

    # plot the assigned landscape
    landscape_plot = sns.scatterplot([i[0] for i in landscape], [i[1] for i in landscape], hue = pointClasses)

    clandMskMat = bts.calcClandMskMat(pointClasses, mskMat)

    # ############################################################################
    # Full network
    # ############################################################################
    # Applies the point-types mask to the migration matrix, and normalizes it to
    #   take into account the movement due to life-stage, and distance.
    # ############################################################################
    network = mntw.normalizeMskMgrMat(migrMat, clandMskMat)
    return network, pointClasses, landscape_plot
