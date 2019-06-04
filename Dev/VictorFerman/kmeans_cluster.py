from sklearn.cluster import KMeans
import numpy as np

coordFileLocation = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/clean/full2.csv"
clusterFileName = '/clusterResult.csv'

coords = []
coordFile = open(coordFileLocation,'r')
for line in coordFile:
    tokens = line.split(',') #long ,lat
    coords.append([float(tokens[0]),float(tokens[1])])
coordFile.close()

patches = len(coords)
clusters = int(patches*0.1)
npCoords = np.array(coords)

clusterResult = KMeans(n_clusters=clusters).fit(npCoords)
centroids = clusterResult.cluster_centers_
labels = clusterResult.labels_

folder= '/'.join(coordFileLocation.split('/')[:-1])
clusterFile = open(folder+clusterFileName, 'w')
for point in centroids:
    clusterFile.write(str(point[0])+','+str(point[1])+'\n')
clusterFile.close()

resultFileName = coordFileLocation.replace('.csv','_clustered.csv')
resultFile = open(resultFileName,'w')
for i in range(patches):
    resultFile.write(str(coords[i][0])+','+str(coords[i][0])+','+str(labels[i])+'\n')
resultFile.close()
