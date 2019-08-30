from random import sample
import numpy as np
import glob
import shutil
import os


sampledNumber = 100
clusterDirs = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/LandAggregated/C*2/"

for clusterDir in sorted(glob.glob(clusterDirs))[:]:

    clusterNum = int(clusterDir.split('/')[-2][1:])
    print(clusterNum)
    clusterFileNames = sorted(glob.glob(clusterDir+'/*_I.csv'))
    sampledFiles = sorted(sample(clusterFileNames, k=sampledNumber))
    for fileName in sampledFiles:
        destination = clusterDir.replace('LandAggregated', 'Clustered')
        if not os.path.exists(destination):
            os.mkdir(destination)
        shutil.copy(fileName, destination)
        shutil.copy(fileName.replace('_I','_S'), destination)
        shutil.copy(fileName.replace('_I','_A'), destination)
