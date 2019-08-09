import glob
import numpy as np
from operator import itemgetter
import vincenty as vn

folder= '/Volumes/marshallShare/ERACR/Yorkeys4/Clustered/'
pattern = 'Yorkeys_CLS_*.csv'
ref_point = (36.617, -119.690) #fowler LL coordinate
#ref_point = (-16.8125, 145.730) #Yorkeys LL coordinate

corner_coord = None
for fileName in sorted(glob.glob(folder+pattern)):
    clusterData = open(fileName,'r')
    clusters = []

    for line in clusterData:
        tokens = line.split(',')
        lat = float(tokens[1])
        long = float(tokens[0])
        cluster = int(tokens[2])
        distance = vn.vincenty(ref_point, (lat,long))
        clusters.append((long,lat,cluster,distance))
    clusterData.close()
    corner_coord = sorted(clusters, key=itemgetter(3))[0]
    print(corner_coord)
