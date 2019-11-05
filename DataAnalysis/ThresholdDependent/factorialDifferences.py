import os
import glob
import numpy as np
import MoNeT_MGDrivE as monet

###############################################################################
# Load compiled CSV and analyze the output
###############################################################################
path = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/Datasets/"
centralFile = "UB.csv"
coverageRescale = 10
sensitivitySelector = 3
if(sensitivitySelector == 1):
    # 001 larval life decrease
    # 002 larval life increase
    title = "Larval Lifespan"
    testFileA = "UBSA_001.csv"
    testFileB = "UBSA_002.csv"
if(sensitivitySelector == 2):
    # 010 adult life increase
    # 020 adult life decrease
    title = "Adult Mortality"
    testFileA = "UBSA_010.csv"
    testFileB = "UBSA_020.csv"
if(sensitivitySelector == 3):
    # 100 fitness cost 10% reduction
    # 200 fitness cost 20% reduction
    title = "Fitness Cost"
    testFileA = "UBSA_100.csv"
    testFileB = "UBSA_200.csv"
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
