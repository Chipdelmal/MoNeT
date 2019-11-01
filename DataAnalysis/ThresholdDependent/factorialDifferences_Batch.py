import os
import glob
import numpy as np
import MoNeT_MGDrivE as monet

def getFilenameFromPath(path):
    return path.split('/')[-1].split('.')[0]

coverageRescale = 10
###############################################################################
# Define paths for central files and sensitivity analysis ones
###############################################################################
pathSA = '/Volumes/marshallShare/ThresholdResub/tnFactorialSA/'
pathCF = '/Volumes/marshallShare/ThresholdResub/tnFactorialSweep/MigrationYes/'
###############################################################################
# Get filepaths and filenames (not in the same sorting!)
###############################################################################
(cfPaths, saPaths) = (
        sorted(glob.glob(pathCF + '*.csv')),
        sorted(glob.glob(pathSA + '*.csv'))
    )
cfFiles = [getFilenameFromPath(i) for i in cfPaths]
saFiles = [getFilenameFromPath(i) for i in saPaths]
###############################################################################
centralFile = cfFiles[0]

centralFile
expCoreID = [i.split('_')[0] for i in saFiles]
matchingIndices = [i == centralFile for i in expCoreID]
###############################################################################
sensitivitySelector = 3
if(sensitivitySelector == 1):
    # 001 larval life decrease
    # 002 larval life increase
    title = "Larval Lifespan"
    testFileA = "UBSA_0001.csv"
    testFileB = "UBSA_0002.csv"
if(sensitivitySelector == 2):
    # 010 adult life increase
    # 020 adult life decrease
    title = "Adult Mortality"
    testFileA = "UBSA_0010.csv"
    testFileB = "UBSA_0020.csv"
if(sensitivitySelector == 3):
    # 100 fitness cost 10% reduction
    # 200 fitness cost 20% reduction
    title = "Fitness Cost"
    testFileA = "UBSA_0100.csv"
    testFileB = "UBSA_0200.csv"
centralData = monet.loadAndHashFactorialCSV(
    path + centralFile, floatMultiplier=coverageRescale
)
probeDataA = monet.loadAndHashFactorialCSV(
    path + testFileA, floatMultiplier=coverageRescale
)
probeDataB = monet.loadAndHashFactorialCSV(
    path + testFileB, floatMultiplier=coverageRescale
)
differencesHashA = monet.calculateFactorialHashError(
    probeDataA,
    centralData,
    monet.sampleDifference
)
differencesHashB = monet.calculateFactorialHashError(
    probeDataB,
    centralData,
    monet.sampleDifference
)
errorsA = differencesHashA.values()
errorsB = differencesHashB.values()

deHashedA = monet.deHashFactorial(differencesHashA)
deHashedB = monet.deHashFactorial(differencesHashB)

np.savetxt(
    path + testFileA.split(".")
    [0] + "Diff.csv", deHashedA, fmt='%2.6f', delimiter=","
)
np.savetxt(
    path + testFileB.split(".")
    [0] + "Diff.csv", deHashedB, fmt='%2.6f', delimiter=","
)
