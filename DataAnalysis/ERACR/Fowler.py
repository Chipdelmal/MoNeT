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


for clsts in [500, 1971]:#[1, 10, 50, 100, 250, 500, 750, 1000, 1250, 1500, 1750, 1971]:
    ##############################################################################
    # Parameters Setup
    ##############################################################################
    (seed, clustersNo, CLST_METHOD) = (42, clsts, 1)
    (lifeStayProb, adultMortality) = (.72, .09)
    PLACE = "Fowler"
    PATH = "/Volumes/marshallShare/ERACR/Fowler4/Clustered/"
    LATLONGS = "fowler_centroids_ordered2.csv"
    namePad = str(clustersNo).rjust(5, '0')
    latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')
    ##############################################################################
    # Clustering Algorithms
    ##############################################################################
    if len(latlongs) == clustersNo:
        clusters = np.array(range(clustersNo))
    else:
        if CLST_METHOD == 1:
            clObj = KMeans(
                n_clusters=clustersNo,
                random_state=seed,
                n_jobs=4
            )
            clustersObj = clObj.fit(latlongs)
            (clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)
        elif CLST_METHOD == 2:
            clObj = AgglomerativeClustering(
                n_clusters=clustersNo,
                affinity='euclidean',
                compute_full_tree='auto',
                memory='mycachedir'
            )
            clustersObj = clObj.fit(latlongs)
            (clusters) = (clustersObj.labels_)
        elif CLST_METHOD == 3:
            clObj = SpectralClustering(
                n_clusters=clustersNo,
                random_state=seed
            )
            clustersObj = clObj.fit(latlongs)
            (clusters) = (clustersObj.labels_)
    ##############################################################################
    # Clustering the pointset
    ##############################################################################
    if len(latlongs) == clustersNo:
        clusters = np.array(range(clustersNo))
    cLatlongs = aux.appendClustersToLatlongs(latlongs, clusters)
    csvPath = PATH + PLACE + "_CLS_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    csvPathSz = PATH + PLACE + "_CLL_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    clustersSizes = [clusters.count(x) for x in range(clustersNo)]
    aux.exportListToCSV(csvPath, cLatlongs)
    np.savetxt(csvPathSz, clustersSizes, fmt='%i', delimiter='\n')
    ##############################################################################
    # Plotting
    ##############################################################################
    plt.figure(figsize=(20, 20))
    plt.scatter(
        latlongs[:, 0], latlongs[:, 1], c=clusters,
        alpha=.25, cmap='hsv', s=150, linewidth=4
    )
    plt.tight_layout()
    plt.xlim(min(latlongs[:, 0]) - .0005, max(latlongs[:, 0]) + .0005)
    plt.ylim(min(latlongs[:, 1]) - .0005, max(latlongs[:, 1]) + .0005)
    plt.savefig(
        PATH + PLACE + "_MAP_" + str(CLST_METHOD) + "_" + namePad + ".png",
        dpi=250
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
    aggrCPath = PATH + PLACE + "_AGC_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    aggrMat = monet.aggregateLandscape(migrMat, clusters, type=1)
    monet.testMarkovMatrix(aggrMat)
    np.savetxt(aggrPath, aggrMat, delimiter=',')
    # np.savetxt(aggrCPath, centroids, delimiter=',')
