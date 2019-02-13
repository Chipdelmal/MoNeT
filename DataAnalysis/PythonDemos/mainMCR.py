import plotly
#NOTE: needs dev version of plotly to work because we use 'stackgroup'
import plotly.graph_objs as go
import plotly.offline as offline
import MoNeT_MGDrivE as monet
offline.init_notebook_mode(connected=True)

###############################################################################
# MCR Experiment Example
###############################################################################

# Define the experiment's path
type = float
experimentString = "E_090_050_010_025"
path = "/Users/sanchez.hmsc/Desktop/ParserDataset/"
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)
# Get the filenames lists
filenames = monet.readExperimentFilenames(path + experimentString)
# Load a single node (Auxiliary function)
nodeIndex = 0
nodeData = monet.loadNodeData(
    filenames.get("male")[nodeIndex],
    filenames.get("female")[nodeIndex],
    dataType=float
)
# Aggregate the whole landscape into one array
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames,
    male=True,
    female=True,
    dataType=float
)
# Aggregate the genotypes of a population
#   (works for a node, or for all the population)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)
# Load the population dynamics data of the whole landscape
landscapeData = monet.loadLandscapeData(filenames, dataType=float)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData,
    aggregationDictionary
)
aggregatedNodesData["landscape"]
###############################################################################
#
###############################################################################
# Plot dynamics in a static plotly set
# tracesList=[]
# for i in range(0,len(columnsList)):
#     trace=go.Scatter(x=range(0,len(aggData)),y=aggData[:,i])
#     tracesList.append(trace)
# offline.iplot(tracesList, filename='basic-line')

labels = aggData["genotypes"]
colors = ["rgb(25,128,255)", "rgb(255,25,128)",
          "rgb(128,0,255)", "rgb(255,0,255)"]
inData = aggData["population"]
tracesList = []
for i in range(0, len(labels)):
    trace = dict(
        x=range(0, len(inData)),
        y=inData[:, i],
        stackgroup='one',
        mode='lines',
        line=dict(width=3, color=colors[i]),
        name=labels[i]
    )
    tracesList.append(trace)
layout = go.Layout(
    title='Genotypes Breakdown',
    xaxis=dict(
        title='Time [days]',
        titlefont=dict(size=20, color='#7f7f7f')
    ),
    yaxis=dict(
        title='Allele Frequency',
        titlefont=dict(size=20, color='#7f7f7f')
    ),
    width=1500,
    height=400
)
#NOTE: needs dev version of plotly to work because of 'stackgroup'
fig = go.Figure(data=go.Data(tracesList), layout=layout)
# py.iplot(fig,filename='stacked-area-plot-hover',validate=False)
plotly.offline.plot(fig, filename='alleleFrequency.html')


labels = aggData["genotypes"]
colors = ["rgb(25,128,255)", "rgb(255,25,128)",
          "rgb(128,0,255)", "rgb(255,0,255)"]
inData = aggData["population"]
tracesList = []
for i in range(0, len(labels)):
    trace = dict(
        x=range(0, len(inData)),
        y=inData[:, i],
        stackgroup='one',
        groupnorm='fraction',
        mode='lines',
        line=dict(width=3, color=colors[i]),
        name=labels[i]
    )
    tracesList.append(trace)
layout = go.Layout(
    title='Genotypes Breakdown',
    xaxis=dict(
        title='Time [days]',
        titlefont=dict(size=20, color='#7f7f7f')
    ),
    yaxis=dict(
        title='Allele Ratio',
        titlefont=dict(size=20, color='#7f7f7f')
    ),
    width=1500,
    height=400
)
fig = dict(data=tracesList, layout=layout)
plotly.offline.plot(fig, filename='allelePercentage.html')

# x[:,2:]
# x[:, [1, 3]]
# columnsList=[[1,1],[1]]
# np.sum(x[:,columnsList[0]],axis=1)
