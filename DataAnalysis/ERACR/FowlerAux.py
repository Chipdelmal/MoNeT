import csv


def appendClustersToLatlongs(latlongs, clusters):
    cLatlongs = [
        [
            latlongs[i][0], latlongs[i][1], clusters[i]
        ] for i in range(len(clusters))
    ]
    return cLatlongs


def exportListToCSV(path, listToExport):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(listToExport)
    return True


def aggregateLandscape(migrationMatrix, clusters):
    return True


if __name__ == "__main__":
    ###########################################################################
    # Load Packages
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import vincenty as vn
    import MoNeT_MGDrivE as monet
    from sklearn.cluster import KMeans
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.cluster import SpectralClustering
    ###########################################################################
    # Setup
    (seed, clustersNo, CLST_METHOD) = (42, 50, 1)
    (lifeStayProb, adultMortality) = (.72, .09)
    PLACE = "Gordonvale"
    PATH = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/GeoLocations/Curated/"
    LATLONGS = "YorkeysKnob_03.csv"
    latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')
    ###########################################################################
    # Clustering Algorithms
    clObj = KMeans(n_clusters=clustersNo, random_state=seed)
    clusters = clObj.fit_predict(latlongs)
    cLatlongs = appendClustersToLatlongs(latlongs, clusters)
    vicClusterObj = clObj.fit(latlongs)
    vicCentroids = vicClusterObj.cluster_centers_
    vicLabels = vicClusterObj.labels_
    ###########################################################################
    # Distance Matrix
    distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
    ###########################################################################
    # Migration Matrix
    zeroInflation = .72 ** .09
    migrMat = monet.zeroInflatedExponentialMigrationKernel(
        distMat,
        params=monet.AEDES_EXP_PARAMS,
        zeroInflation=lifeStayProb ** adultMortality
    )
    ###########################################################################
    # Aggregation
    # sitesNum = len(latlongs)
    # clustersID = sorted(set(clusters))
    # clustersNum = len(clustersID)
    # aggrdMat = np.zeros([clustersNum, clustersNum], dtype=float)
    # grpdClust = [list(np.where(clusters == id)[0]) for id in clustersID]
    # grpdLens = [len(clst) for clst in grpdClust]
    #
    # for row in range(clustersNum):
    #     rowGroup = grpdClust[row]
    #     for col in range(clustersNum):
    #         aggrdMat[row, col] = sum(migrMat[rowGroup][grpdClust[col]])
    #     aggrdMat[row] = aggrdMat[row] / grpdLens[row]
    #
    # sum(aggrdMat[1])
    # monet.testMarkovMatrix(migrMat)

    num_clusters = len(vicCentroids)
    aggr_matrix = np.zeros([num_clusters, num_clusters], dtype=float)
    aggr_latlongs = [[] for x in range(num_clusters)]
    for idx, label in enumerate(vicLabels):
        aggr_latlongs[label].append(idx)
    for row in range(num_clusters):
        row_ids = aggr_latlongs[row]
        for colum in range(num_clusters):
            colum_ids  =aggr_latlongs[colum]
            res = 0
            for rid in row_ids:
                for cid in colum_ids:
                    res += migrMat[rid][cid]
            aggr_matrix[row][colum] = res/len(row_ids)

    print(sum(aggr_matrix[1]))
    monet.testMarkovMatrix(aggr_matrix)
