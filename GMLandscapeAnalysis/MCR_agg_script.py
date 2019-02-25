import plotly #NOTE: needs dev version of plotly (because of 'stackgroup')
import plotly.graph_objs as go
import plotly.offline as offline
import MoNeT_MGDrivE as monet
import plotly.plotly as py
offline.init_notebook_mode(connected=True)


###############################################################################
# MCR Construct
###############################################################################
#------------------------------------------------------------------------------
# Data Handling
#------------------------------------------------------------------------------
ITERATIONS = 10
time_to_thres = []
for i in range(1, ITERATIONS+1):
    #print(i)
    # Define the experiment's path, aggregation dictionary, and read filenames
    type = float
    formatted_num = '%03d' % i
    #experimentString = "E_095_075_006_015"
    #path = "/Users/sanchez.hmsc/odrive/sanchez.hmsc@berkeley.edu/GMLandscape/ParserDataset/"
    experimentString = "E_099_000_000_"+formatted_num

    path = "/Users/Biyonka/Desktop/Output/2019_02_25_ANALYZED/"
    aggregationDictionary = monet.generateAggregationDictionary(
        ["W", "H", "R", "B"],
        [
            [0, 0, 1, 2, 3],    # Wild
            [1, 4, 4, 5, 6],    # Homing
            [2, 5, 7, 7, 8],    # Resistant
            [3, 6, 8, 9, 9]     # Broken
        ]
    )
    filenames = monet.readExperimentFilenames(path + experimentString)
    # To analyze a single node ...................................................
    # Load a single node (auxiliary function just for demonstration)
    # nodeIndex = 0
    # nodeData = monet.loadNodeData(
    #     filenames.get("male")[nodeIndex],
    #     filenames.get("female")[nodeIndex],
    #     dataType=float
    # )

    # To analyze the sum of the whole landscape ..................................
    # Sum landscape into one array ("in place" memory-wise)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames,
        male=True,
        female=True,
        dataType=float
    )

    # Aggregate genotypes (node or landscape) ....................................
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )

    # To analyze the landscape without sum .......................................
    # Load the population dynamics data of the whole landscape
    # landscapeData = monet.loadLandscapeData(filenames, dataType=float)
    # aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    #     landscapeData,
    #     aggregationDictionary
    # )
    # aggregatedNodesData["landscape"]

    #get wild type proportion at end
    wbh = aggData['population'][:, 0] + aggData['population'][:, 1] + aggData['population'][:, 3]
    ratio_homing = aggData['population'][:, 1]/(wbh)
    #get time at which homing ratio exceeds threshold
    time = (list(ratio_homing>0.1)).index(True)
    time_to_thres.append(time)
{'iteration': range(1, ITERATIONS+1, 1), 'time_to_thres': time_to_thres}
#------------------------------------------------------------------------------
# Plotting
#------------------------------------------------------------------------------

labels = aggData["genotypes"]
colors = ["rgb(25,128,255)", "rgb(255,25,128)",
          "rgb(128,0,255)", "rgb(255,0,255)"]
inData = aggData["population"]

# Plot allele frequency dynamics .............................................
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
fig = go.Figure(data=go.Data(tracesList), layout=layout)
py.iplot(fig,filename='stacked-area-plot-hover',validate=False)
plotly.offline.plot(fig, filename='alleleFrequency.html')


# Plot allele ratio dynamics ..................................................
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
