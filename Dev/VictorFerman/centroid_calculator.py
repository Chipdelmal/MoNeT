import glob
import numpy as np

folder= '/Volumes/marshallShare/ERACR/Yorkeys4/Clustered/'
pattern = 'Yorkeys_CLS_*.csv'

for fileName in sorted(glob.glob(folder+pattern)):
    clusterData = open(fileName,'r')
    clusters = {}
    for line in clusterData:
        tokens = line.split(',')
        lat = float(tokens[1])
        long = float(tokens[0])
        cluster = int(tokens[2])
        if not cluster in clusters:
            clusters[cluster]={'lats':[], 'longs':[]}
        clusters[cluster]['lats'].append(lat)
        clusters[cluster]['longs'].append(long)
    clusterData.close()
    centroids = []
    for i in range(len(clusters)):
        mlat = np.mean(clusters[i]['lats'])
        mlong = np.mean(clusters[i]['longs'])
        centroids.append((mlong,mlat))

    resultFileName = fileName.replace('_CLS_','_AGCV_')
    resultFile = open(resultFileName,'w')
    for i in range(len(centroids)):
        resultFile.write(str(centroids[i][0])+','+str(centroids[i][1])+'\n')
    resultFile.close()
