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
    num_clusters = len(set(clusters))
    aggr_matrix = np.zeros([num_clusters, num_clusters], dtype=float)
    aggr_latlongs = [[] for x in range(num_clusters)]
    for idx, label in enumerate(clusters):
        aggr_latlongs[label].append(idx)
    for row in range(num_clusters):
        row_ids = aggr_latlongs[row]
        for colum in range(num_clusters):
            colum_ids = aggr_latlongs[colum]
            res = 0
            for rid in row_ids:
                for cid in colum_ids:
                    res += migrationMatrix[rid][cid]
            aggr_matrix[row][colum] = res/len(row_ids)
    return aggr_matrix

def aggregateLandscapeAltVic(migrationMatrix, clusters):
    matrix_size = len(clusters)
    num_clusters = len(set(clusters))
    aggr_matrix = np.zeros([num_clusters, num_clusters], dtype=float)
    aggr_number = [0]*num_clusters
    for row in range(matrix_size):
        cRow = clusters[row]
        aggr_number[cRow] +=1
        for col in range(matrix_size):
            cCol = clusters[col]
            aggr_matrix[cRow][cCol] += migrationMatrix[row][col]
    for row in range(num_clusters):
        aggr_matrix[row] = [x/aggr_number[row] for x in aggr_matrix[row]]
    return aggr_matrix



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
    clustersObj = clObj.fit(latlongs)
    (clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)
    cLatlongs = appendClustersToLatlongs(latlongs, clusters)
    ###########################################################################
    # Distance Matrix
    distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
    ###########################################################################
    # Migration Matrix
    zeroInflation = pow(.72, .09)
    migrMat = monet.zeroInflatedExponentialMigrationKernel(
        distMat,
        params=monet.AEDES_EXP_PARAMS,
        zeroInflation=lifeStayProb ** adultMortality
    )
    ###########################################################################
    # Aggregation
    aggregatedMatrix = aggregateLandscape(migrMat, clusters)
    monet.testMarkovMatrix(aggregatedMatrix)
