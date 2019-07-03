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
