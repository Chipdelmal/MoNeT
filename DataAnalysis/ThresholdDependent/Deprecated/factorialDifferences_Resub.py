# import plotly.offline as offline
# import plotly.graph_objs as go
# import plotly
import numpy as np
import MoNeT_MGDrivE as monet
# offline.init_notebook_mode(connected=True)

###############################################################################
# Load compiled CSV and analyze the output
###############################################################################
pathC = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/Datasets/"
pathE = "/Volumes/marshallShare/ThresholdResub/"
drive = "U"
centralFile = drive + "Xxx.csv"
coverageRescale = 10
sensitivitySelector = 1
###############################################################################
if(sensitivitySelector == 1):
    # 001 Migration Decrease
    # 002 Migration Increase
    title = "Migration"
    base = "factorialSensitivity/"
    testFileA = base + drive + "XSA_0001.csv"
    testFileB = base + drive + "XSA_0002.csv"
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
###############################################################################
centralData = monet.loadAndHashFactorialCSV(
    pathC + centralFile, floatMultiplier=coverageRescale
)
probeDataA = monet.loadAndHashFactorialCSV(
    pathE + testFileA, floatMultiplier=coverageRescale
)
probeDataB = monet.loadAndHashFactorialCSV(
    pathE + testFileB, floatMultiplier=coverageRescale
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
###############################################################################
deHashedA = monet.deHashFactorial(differencesHashA)
deHashedB = monet.deHashFactorial(differencesHashB)
###############################################################################
np.savetxt(
    pathE + testFileA.split(".")
    [0] + "Diff.csv", deHashedA, fmt='%2.6f', delimiter=","
)
np.savetxt(
    pathE + testFileB.split(".")
    [0] + "Diff.csv", deHashedB, fmt='%2.6f', delimiter=","
)
###############################################################################
