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
    (seed, clustersNo, CLST_METHOD) = (42, 250, 1)
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
    sitesNum = len(latlongs)
    clustersID = sorted(set(clusters))
    clustersNum = len(clustersID)
    aggrdMat = np.zeros([clustersNum, clustersNum], dtype=float)
    grpdClust = [list(np.where(clusters == id)[0]) for id in clustersID]
    grpdLens= [len(clst) for clst in groupedClusters]



    for row in range(clustersNum):
        for col in range(clustersNum):
            group = clustersID[col]
            currNodes = grpdClust[group]
            aggrdMat[row, col] = sum(migrMat[row][currNodes])
    aggrdMat
