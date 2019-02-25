import plotly.offline as offline
import plotly.graph_objs as go
import plotly
import numpy as np
import MoNeT_MGDrivE as monet
offline.init_notebook_mode(connected=True)

###############################################################################
# Load compiled CSV and analyze the output
###############################################################################
path = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/Datasets/"
centralFile = "UB.csv"
coverageRescale = 10
sensitivitySelector = 2
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

###############################################################################
# Plotting the results
###############################################################################
# binsDict = dict(start=0, end=1, size=0.05)
# trace1 = go.Histogram(
#     x=errorsA, histnorm='percent',
#     name='Increase', xbins=binsDict,
#     marker=dict(color='#B9C1DB'), opacity=0.75
# )
# trace2 = go.Histogram(
#     x=errorsB, histnorm='percent',
#     name='Decrease', xbins=binsDict,
#     marker=dict(color='#FF7373'), opacity=0.75
# )
# layout = go.Layout(
#     title=title, xaxis=dict(title='Difference'),
#     yaxis=dict(title='Count'), bargap=0.125, bargroupgap=0.05
# )
# data = [trace1, trace2]
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.iplot(fig, filename='normalized histogram')
