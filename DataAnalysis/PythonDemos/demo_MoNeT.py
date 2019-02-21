import plotly #NOTE: needs dev version of plotly (because of 'stackgroup')
import plotly.graph_objs as go
import plotly.offline as offline
import MoNeT_MGDrivE as monet
import plotly.plotly as py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
offline.init_notebook_mode(connected=True)


def plotMeanGenotypeTrace(aggData, style):
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df=pd.DataFrame(time , columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local=pd.DataFrame(pops, columns=groups)
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=0.5)
    #plt.xticks([])
    #plt.yticks([])
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')

    for i in range(len(final)):
        final[i].plot(ax = ax, linewidth = style["width"], legend=False, color = colors[i], alpha =style["alpha"])


    legends=[]
    for i in range(len(groups)):
        legends.append(
            mpatches.Patch(color=colors[i], label=groups[i])
        )
    #plt.legend(handles=legends)
    #ax.xaxis.set_label_text("")
    #ax.yaxis.set_label_text("")
    plt.ylabel("Allele Count")

    return plt

###############################################################################
# MCR Construct
###############################################################################

#------------------------------------------------------------------------------
# Data Handling
#------------------------------------------------------------------------------

# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_095_075_006_015"
path = "/Users/sanchez.hmsc/odrive/sanchez.hmsc@berkeley.edu/GMLandscape/ParserDataset/"
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

#------------------------------------------------------------------------------
# Plotting
#------------------------------------------------------------------------------

style={
    "width":2,
    "alpha":1,
    "dpi":1024,
    "legend":True,
    "colors": [
        '#5cf64a', '#6e44ff','#e56399','#f1866d', '#861657',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}
plt=plotMeanGenotypeTrace(aggData,style)
plt.savefig("./images/demotraces.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=False, bbox_inches='tight',
            pad_inches=0, frameon=None)
plt.close(fig)
plt.close('all')


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
