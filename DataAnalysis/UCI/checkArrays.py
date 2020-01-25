#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
import MoNeT_MGDrivE as monet


def returnArraysShapes(filePaths):
    shps = []
    for file in filePaths:
        tmp = np.loadtxt(file, skiprows=1, delimiter=',')
        shps.append(tmp.shape)
    return set(shps)


PATH_ROOT = '/Volumes/marshallShare/UCI/STP/out/stp_kernel_elevation_v3_balanced/'
folders = ('ANALYZED/0001', 'GARBAGE/0001/')

# Mean analysis verification
files = monet.readExperimentFilenames(PATH_ROOT + folders[0])
mShapes = returnArraysShapes(files['male'])
fShapes = returnArraysShapes(files['female'])

if (len(mShapes) == 1 and len(fShapes) == 1):
    print('Mean passed!')
else:
    print('Mean failed!')


shps = []
fldrs = monet.listDirectoriesWithPathWithinAPath(PATH_ROOT + folders[1])
for fld in fldrs:
    files = monet.readExperimentFilenames(fld)
    shps.append((
            returnArraysShapes(files['male']),
            returnArraysShapes(files['female'])
        ))
