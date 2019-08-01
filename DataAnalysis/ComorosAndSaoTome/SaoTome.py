import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ComorosAux as aux
import vincenty as vn
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering


# for clsts in [1, 1000, 2000, 3000]:
clsts = -1
###########################################################################
# Parameters Setup
###########################################################################
(seed, clustersNo, CLST_METHOD) = (int(time.time()), clsts, 1)
(lifeStayProb, adultMortality) = (.72, .09)
PLACE = "Comoros"
PATH = "/Volumes/marshallShare/Comoros_STP/STP/"
LATLONGS = "stp_sites_v1.csv"
###############################################################################
###############################################################################
#clsustersNo = -1
for clustersNo in [-1, 1, 10, 50, 75, 100, 125, 145]:
    geoData = np.genfromtxt(
            PATH + LATLONGS,
            delimiter=',',
            usecols=[2, 1, 3],
            skip_header=1,
            encoding="UTF-8"
    )
    latlongs = geoData[:,:2]
    pops = geoData[:, 2]
    if clustersNo == -1:
        namePad = str(len(latlongs)).rjust(5, '0')
    else:
        namePad = str(clustersNo).rjust(5, '0')
    ###########################################################################
    # Clustering Algorithms
    ###########################################################################
    if clustersNo == -1:
        clusters = np.array(range(len(latlongs)))
    else:
        if CLST_METHOD == 1:
            clObj = KMeans(
                n_clusters=clustersNo,
                random_state=seed,
                n_jobs=4
            )
            clustersObj = clObj.fit(latlongs)
            (clusters, centroids) = (
                    clustersObj.labels_,
                    clustersObj.cluster_centers_
                )
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
    ###########################################################################
    # Clustering the pointset
    ###########################################################################
    cLatlongs = aux.appendClustersToLatlongs(latlongs, clusters)
    csvPath = PATH + PLACE + "_CLS_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    csvPathSz = PATH + PLACE + "_CLL_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    clustersSizes = [sorted(clusters).count(x) for x in range(clustersNo)]
    aux.exportListToCSV(csvPath, cLatlongs)
    np.savetxt(csvPathSz, clustersSizes, fmt='%i', delimiter='\n')
    ###########################################################################
    # Plotting
    ###########################################################################
    plt.figure(figsize=(25, 20))
    plt.scatter(
        latlongs[:, 0], latlongs[:, 1], c=clusters,
        alpha=.25, cmap='hsv', s=(pops/10), linewidth=4
    )
    plt.tight_layout()
    plt.xlim(min(latlongs[:, 0]) - .05, max(latlongs[:, 0]) + .05)
    plt.ylim(min(latlongs[:, 1]) - .05, max(latlongs[:, 1]) + .05)
    plt.savefig(
        PATH + PLACE + "_MAP_" + str(CLST_METHOD) + "_" + namePad + ".png",
        dpi=500
    )
    plt.close()
    ###########################################################################
    # Export distance matrix
    ###########################################################################
    distPath = PATH + PLACE + "_DST_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
    # np.savetxt(distPath, distMat.astype(int), fmt='%i', delimiter=',')
    # heat = sns.heatmap(distMat, annot=False)
    # heat.get_figure().savefig(PATH + PLACE + "DIST.png", dpi=500)
    ###########################################################################
    # Export migration matrix
    ###########################################################################
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
    ###########################################################################
    # Export aggregated migration matrix
    ###########################################################################
    aggrPath = PATH + PLACE + "_AGG_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    aggrCPath = PATH + PLACE + "_AGC_" + str(CLST_METHOD) + "_" + namePad + ".csv"
    aggrMat = monet.aggregateLandscape(migrMat, clusters)
    monet.testMarkovMatrix(aggrMat)
    np.savetxt(aggrPath, aggrMat, delimiter=',')
    # np.savetxt(aggrCPath, centroids, delimiter=',')
