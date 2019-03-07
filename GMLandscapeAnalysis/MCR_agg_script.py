import plotly #NOTE: needs dev version of plotly (because of 'stackgroup')
import plotly.graph_objs as go
import plotly.offline as offline
import MoNeT_MGDrivE as monet
import plotly.plotly as py
import numpy as np
import pandas as pd
offline.init_notebook_mode(connected=True)


###############################################################################
# MCR Construct
###############################################################################
#------------------------------------------------------------------------------
# Analyzing different metrics on drive behavior
#------------------------------------------------------------------------------
experiments = ['BASE', 'LOOSE', 'TIGHT', 'UNEVEN']
time_to_thres, intersection, prop_homing_end = [], [], []
for i in experiments:
    # Define the experiment's path, aggregation dictionary, and read filenames
    type = float
    experimentString = "E_099_000_000_001"
    path = "/Users/Biyonka/Desktop/Output/contrived_landscapes/" + i + "_2019_02_27_ANALYZED/"
    aggregationDictionary = monet.generateAggregationDictionary(
        ["W", "H", "R", "B"],
        [
            [0, 0, 1, 2, 3],
            [1, 4, 4, 5, 6],
            [2, 5, 7, 7, 8],
            [3, 6, 8, 9, 9]
        ]
    )
    filenames = monet.readExperimentFilenames(path + experimentString)

    # To analyze a single node ...................................................
    # Load a single node (auxiliary function just for demonstration)
    nodeIndex = 0
    nodeData = monet.loadNodeData(
        filenames.get("male")[nodeIndex], filenames.get("female")[nodeIndex],
        dataType=float
    )

    # To analyze the sum of the whole landscape ..................................
    # Sum landscape into one array ("in place" memory-wise)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )

    # Aggregate genotypes (node or landscape) ....................................
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )
    wbh = np.sum(aggData['population'], axis =1)
    ratio_homing = aggData['population'][:, 1]/(wbh)
    #get time at which homing ratio exceeds threshold
    if any(ratio_homing >= 0.5):
        #get first time that ratio exceeds 0.5
        time = (list(ratio_homing> 0.5)).index(True)
    else:
        # if threshold of homing never eceeds 0.5, set time to
        #total length of experiment (i.e. 3 years)
        time = aggData['population'].shape[0]
    time_to_thres.append(time)

    #get proportion of homing at end of 3 years
    prop_homing = aggData['population'][:, 1][-1]/wbh[-1]
    prop_homing_end.append(prop_homing)

    #get the time of intersection between wild and homing
    diff = aggData['population'][:, 1] - aggData['population'][:, 0]
    if i == "TIGHT":
        #no intersection occurs in the tight experiment
        inter = aggData['population'].shape[0]
    else:
        #get index where the wild and homing arrays are the closest
        inter = list(np.abs(diff)).index(min(np.abs(diff)))
    intersection.append(inter)

metrics_df = pd.DataFrame({'experiment': experiments,
'time_to_thres': time_to_thres,
'intersection': intersection,
'prop_homing_end': prop_homing_end})
metrics_df['num_inflection'] = [1, 2, 1, 2]
metrics_df.to_csv("metrics.csv", header = True, index = False)
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
