import os
import glob
import numpy as np

pathRoot = "/Volumes/marshallShare/ERACR/Bakersfield/Full"

clusterFile='/Volumes/marshallShare/ERACR/Bakersfield/Full/clustered/pusheen11081.csv'
lats = []
longs = []
clusters = []

clusterData = open(clusterFile,'r')
next(clusterData)
for line in clusterData:
    tokens = line.split(',')
    lat = float(tokens[0])
    long = float(tokens[1])
    cluster = int(tokens[2])
    lats.append(lat)
    longs.append(long)
    clusters.append(cluster)

minLat = min(lats)
index = lats.index(minLat)
print(lats[index],longs[index], clusters[index])
