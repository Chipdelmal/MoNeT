import csv
import itertools

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

def aggregateLandscape_gillian(migrationMatrix, clusters):
    num_clusters = len(set(clusters))
    aggr_matrix = np.zeros([num_clusters, num_clusters], dtype=float)
    aggr_latlongs = [[] for x in range(num_clusters)]

    # get all the patches that fall under each label
    [aggr_latlongs[label].append(idx) for idx, label in enumerate(clusters)]

    # get the number of patches in each label for normalization later
    normVal = dict()
    for idx, label in enumerate(clusters):
        normVal[label] = len(aggr_latlongs[label])

    for row in range(num_clusters):
        row_ids = aggr_latlongs[row]
        for column in range(num_clusters):
            colum_ids = aggr_latlongs[colum]
            all_comb = [migrationMatrix[x][y] for x, y in [itertools.product([row_ids, colum_ids])]]
            aggr_matrix[row][column] = sum(all_comb)/len(row_ids)
    return aggr_matrix

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

def agglom_clustering(points, pop, num_clusters, method="Kmeans"):
    # dat_pos, dat_pop = dat[0:1], dat[2]

    list_of_centroids = []
    for i in num_clusters:
    # for i in range(1, 100, 10):
        # clustering = AgglomerativeClustering(n_clusters=i).fit(points)
        if method == "Kmeans":
            clObj = KMeans(n_clusters=i, random_state=seed)
            clustersObj = clObj.fit(latlongs)
            (clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)
            cLatlongs = appendClustersToLatlongs(latlongs, clusters)

        if method == "Agglomerative": 
            clObj = AgglomerativeClustering(n_clusters=i)
            clustering = clObj.fit(latlongs)
            
            clusters = clustering.labels_
            cLatlongs = appendClustersToLatlongs(latlongs, clusters)

        # saving the coords
        with open('FowlerResults/'+str(i)+method+'AggregationCoord.csv', mode='w') as destination:
            writer = csv.writer(destination, delimiter= ',')
            for i in cLatlongs:
                writer.writerow(i)


if __name__ == "__main__":
    ###########################################################################
    # Load Packages
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import vincenty as vn
    # import MoNeT_MGDrivE as monet
    from sklearn.cluster import KMeans
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.cluster import SpectralClustering
    ###########################################################################
    # Setup
    (seed, clustersNo, CLST_METHOD) = (42, 50, 1)
    (lifeStayProb, adultMortality) = (.72, .09)
    PLACE = "Fowler"
    # PATH = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/GeoLocations/Curated/"
    LATLONGS = "FowlerCLS1.csv"
    data = np.genfromtxt(LATLONGS, delimiter=',')
    ###########################################################################
    # Clustering Algorithms
    # clObj = KMeans(n_clusters=clustersNo, random_state=seed)
    # clustersObj = clObj.fit(latlongs)
    # (clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)
    # cLatlongs = appendClustersToLatlongs(latlongs, clusters)
    ###########################################################################
    # Clustering to Different Levels
    ###########################################################################
    latlongs = data[:,:2]
    sizes = data[:, 2:]
    num_clusters = [1, 250, 500, 750, 1000, 1250, 1500, 1971]
    method = "Kmeans"
    centroids = agglom_clustering(latlongs, sizes, num_clusters, method=method)    
    print("centroids are created")

    ###########################################################################
    # Distance Matrix
    # distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
    ###########################################################################
    # Migration Matrix
    # zeroInflation = pow(.72, .09)
    # migrMat = monet.zeroInflatedExponentialMigrationKernel(
    #     distMat,
    #     params=monet.AEDES_EXP_PARAMS,
    #     zeroInflation=lifeStayProb ** adultMortality
    # )
    ###########################################################################
    # Aggregation
    # aggregatedMatrix = aggregateLandscape(migrMat, clusters)
    # monet.testMarkovMatrix(aggregatedMatrix)

    # distPath = PATH + PLACE + "AGG.csv"
    # # aggMat =monet.aggregateLandscape_gillian(migrationMatrix, clusters)
    # np.savetxt(aggPath, aggMat, delimiter=',')

