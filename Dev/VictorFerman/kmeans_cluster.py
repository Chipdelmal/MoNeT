from sklearn.cluster import KMeans
import numpy as np
from operator import itemgetter

coordFileLocation = "//Volumes/marshallShare/ERACR/Fowler/fowler_centroids.csv"
clusterFileName = '/clusteringResult2.csv'

coords = []
coordFile = open(coordFileLocation,'r')
for line in coordFile:
    tokens = line.split(',') #long ,lat
    coords.append([float(tokens[0]),float(tokens[1])])
coordFile.close()

sCoords = sorted(coords, key=itemgetter(1,0))

patches = len(sCoords)
clusters = int(patches*0.3)
npCoords = np.array(sCoords)

clusterResult = KMeans(n_clusters=clusters).fit(npCoords)
centroids = clusterResult.cluster_centers_
labels = clusterResult.labels_


resultFileName = coordFileLocation.replace('.csv','_ordered2.csv')
resultFile = open(resultFileName,'w')
for i in range(patches):
    resultFile.write(str(sCoords[i][0])+','+str(sCoords[i][1])+'\n')
resultFile.close()

folder= '/'.join(coordFileLocation.split('/')[:-1])
clusterFile = open(folder+clusterFileName, 'w')
for point in centroids:
    clusterFile.write(str(point[0])+','+str(point[1])+'\n')
clusterFile.close()

resultFileName = coordFileLocation.replace('.csv','_clustered2.csv')
resultFile = open(resultFileName,'w')
for i in range(patches):
    resultFile.write(str(coords[i][0])+','+str(coords[i][1])+','+str(labels[i])+'\n')
resultFile.close()
