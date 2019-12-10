import os
import numpy as np
import itertools
# import random
import seaborn as sns
import aux as aux
import bouts as bts
import network as mntw
import landscape as land
import MoNeT_MGDrivE as monet
#import matplotlib.pyplot as plt


def genSingle(n, zeroInflation, landscapeProb, mskMat):
    (lo, hi, n) = (0, 50, n)
    # ############################################################################
    # Mosquito biological behaviour
    # ############################################################################
    # mskMat: This matrix defines how probable is for a mosquito to
    #   move from one life stage to the next (and, as a consequence, from a site
    #   type to the next).
    # ############################################################################
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
        zeroInflation=0.75
    )
    aux.testMarkovMat(migrMat)

    # ############################################################################
    # Point types
    # ############################################################################
    # Assigns classes types to the points in the landscape (this routine will
    #   fail if there's few points with respect to the dimension of the point
    #   types)
    # ############################################################################
    # pointClasses = bts.genURandLandscapeClasses(len(mskMat), n)
    pointClasses = bts.genMRandLanscapeClasses(len(mskMat), n, landscapeProb)
    # plot the assigned landscape
    landscape_plot = sns.scatterplot(
            [i[0] for i in landscape],
            [i[1] for i in landscape],
            hue=pointClasses, legend=False
        )
    clandMskMat = bts.calcClandMskMat(pointClasses, mskMat)
    # print(clandMskMat)

    # ############################################################################
    # Full network
    # ############################################################################
    # Applies the point-types mask to the migration matrix, and normalizes it
    #   to take into account the movement due to life-stage, and distance.
    # ############################################################################
    network = mntw.normalizeMskMgrMat(migrMat, clandMskMat)
    return (network, pointClasses, landscape_plot)


def genCSV(reps, n, heterogenity, landscapeProb, mskMat, zeroInflation):
    params = list(itertools.product(n, heterogenity, landscapeProb))
    delimiter = '_'

    # create number of reps simulations
    for i in range(1, reps+1):
        for (j, zeroInflation, prob) in params:
            singleMatrix, pointClasses, landscapePlot = genSingle(
                j, zeroInflation, prob, mskMat
            )
            # produce the name composed of probability
            s = '-'
            probInNames = s.join([str(int(p*100)).rjust(3, '0') for p in prob])
            baseName = delimiter.join(
                    [
                        str(j), probInNames,
                        str(i).rjust(4, '0').rjust(3, '0')
                    ]
                )
            # save the simulated data as csv files
            filename = delimiter.join(['H', baseName])
            filenameTypes = delimiter.join(['T', baseName])

            # save kernel files
            np.savetxt(
                    "kernels" + os.sep + filename + ".csv",
                    singleMatrix, delimiter=","
                )

            # save figure
            filenameLand = "kernels" + os.sep + 'H_' + baseName + '.png'
            fig = landscapePlot.get_figure()
            fig.savefig(filenameLand)
