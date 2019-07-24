import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import FowlerAux as aux
import vincenty as vn
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering
from itertools import groupby


for clsts in [1, 25, 50, 250, 500, 750, 1000, 1250, 1500, 2000]:
    ##############################################################################
    # Parameters Setup
    ##############################################################################
    (seed, clustersNo, CLST_METHOD) = (42, clsts, 1)
    (lifeStayProb, adultMortality) = (.72, .09)
    # PLACE = "BakersfieldRiver"
    # PATH = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/clean/"
    # LATLONGS = "full2.csv"
    PLACE = "Yorkeys"
    PATH = "/Volumes/marshallShare/ERACR/Yorkeys/Clustered/"
    LATLONGS = "YorkeysKnob_01.csv"
    # PLACE = "Gordonvale"
    # PATH = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/GeoLocations/Curated/"
    # LATLONGS = "YorkeysKnob_03.csv"
    # PLACE = "Fowler"
    # PATH = "/Volumes/marshallShare/ERACR/Fowler/"
    # LATLONGS = "fowler_centroids.csv"
    namePad = str(clustersNo).rjust(5, '0')
    latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')
    ##############################################################################
    # Clustering Algorithms
    ##############################################################################
    if CLST_METHOD == 1:
        clObj = KMeans(
            n_clusters=clustersNo,
            random_state=seed
        )
    elif CLST_METHOD == 2:
        clObj = AgglomerativeClustering(
            n_clusters=clustersNo,
            affinity='euclidean',
            compute_full_tree='auto'
        )
    elif CLST_METHOD == 3:
        clObj = SpectralClustering(
            n_clusters=clustersNo,
            random_state=seed
        )
    clustersObj = clObj.fit(latlongs)
    (clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)
    ##############################################################################
    # Clustering the pointset
    ##############################################################################
    cLatlongs = aux.appendClustersToLatlongs(latlongs, clusters)
    csvPath = PATH + PLACE + "_CLS_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    csvPathSz = PATH + PLACE + "_CLL_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    clustersSizes = [sorted(clusters).count(x) for x in range(clustersNo)]
    aux.exportListToCSV(csvPath, cLatlongs)
    np.savetxt(csvPathSz, clustersSizes, fmt='%i', delimiter='\n')
    ##############################################################################
    # Plotting
    ##############################################################################
    plt.figure(figsize=(35, 20))
    plt.scatter(
        latlongs[:, 0], latlongs[:, 1], c=clusters,
        alpha=.25, cmap='hsv', s=150, linewidth=4
    )
    plt.tight_layout()
    plt.xlim(min(latlongs[:, 0]) - .0005, max(latlongs[:, 0]) + .0005)
    plt.ylim(min(latlongs[:, 1]) - .0005, max(latlongs[:, 1]) + .0005)
    plt.savefig(
        PATH + PLACE + "_MAP_" + str(CLST_METHOD) + "_" + namePad + ".png",
        dpi=500
    )
    plt.close()
    ##############################################################################
    # Export distance matrix
    ##############################################################################
    distPath = PATH + PLACE + "_DST_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
    # np.savetxt(distPath, distMat.astype(int), fmt='%i', delimiter=',')
    # heat = sns.heatmap(distMat, annot=False)
    # heat.get_figure().savefig(PATH + PLACE + "DIST.png", dpi=500)
    ##############################################################################
    # Export migration matrix
    ##############################################################################
    migrPath = PATH + PLACE + "_MIG_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    zeroInflation = pow(lifeStayProb, adultMortality)
    migrMat = monet.zeroInflatedExponentialMigrationKernel(
        distMat,
        params=monet.AEDES_EXP_PARAMS,
        zeroInflation=zeroInflation
    )
    monet.testMarkovMatrix(migrMat)
    # np.savetxt(migrPath, migrMat, delimiter=',')
    # heat = sns.heatmap(migrMat, annot=False)
    # heat.get_figure().savefig(PATH + "MIGR.png", dpi=500)
    ##############################################################################
    # Export aggregated migration matrix
    ##############################################################################
    aggrPath = PATH + PLACE + "_AGG_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    aggrCPath = PATH + PLACE + "_AGC_" + str(CLST_METHOD) + namePad + ".csv"
    aggrMat = monet.aggregateLandscape(migrMat, clusters)
    monet.testMarkovMatrix(aggrMat)
    np.savetxt(aggrPath, aggrMat, delimiter=',')
    np.savetxt(aggrCPath, centroids, delimiter=',')
