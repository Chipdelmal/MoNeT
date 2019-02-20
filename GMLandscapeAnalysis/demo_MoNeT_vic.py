# import plotly #NOTE: needs dev version of plotly (because of 'stackgroup')
# import plotly.graph_objs as go
# import plotly.offline as offline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet
#import plotly.plotly as py
#offline.init_notebook_mode(connected=True)

###############################################################################
# MCR Construct
###############################################################################


def vicGraphs(aggData):
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df=pd.DataFrame(time , columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local=pd.DataFrame(pops, columns=groups)
    colors = ['#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']
    fig, ax = plt.subplots()
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')

    for i in range(len(final)):
        final[i].plot(ax = ax, linewidth = 0.3, legend=False, color = colors[i], alpha = 0.5)
    W_patch = mpatches.Patch(color='#6e44ff', label='W')
    H_patch = mpatches.Patch(color='#e56399', label='H')
    R_patch = mpatches.Patch(color='#ee6c4d', label='R')
    B_patch = mpatches.Patch(color='#861657', label='B')
    plt.legend(handles=[W_patch, H_patch,R_patch,B_patch])
    plt.ylabel("Allele Count")
    plt.savefig("demotraces.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches='tight',
                pad_inches=0.05, frameon=None)
    plt.close(fig)
    plt.close('all')

    fig, ax2 = plt.subplots()
    allele_dict = {}
    for i in range(len(groups)):
        allele_dict[groups[i]] = final[i].T.sum()
    res = pd.DataFrame(allele_dict)
    res.plot(kind = 'area', ax =ax2, color=colors)
    plt.savefig("demostack.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches='tight',
                pad_inches=0.05, frameon=None)
    plt.close(fig)
    plt.close('all')


#------------------------------------------------------------------------------
# Data Handling
#------------------------------------------------------------------------------

# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_095_075_006_015"
path = "/Users/vferman/Downloads/"
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],# Wild
        [1, 4, 4, 5, 6],# Homing
        [2, 5, 7, 7, 8],# Resistant
        [3, 6, 8, 9, 9]# Broken
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
vicGraphs(aggData)
labels = aggData["genotypes"]
colors = ["rgb(25,128,255)", "rgb(255,25,128)",
          "rgb(128,0,255)", "rgb(255,0,255)"]
inData = aggData["population"]

# Plot allele frequency dynamics .............................................
# tracesList = []
# for i in range(0, len(labels)):
#     trace = dict(
#         x=range(0, len(inData)),
#         y=inData[:, i],
#         stackgroup='one',
#         mode='lines',
#         line=dict(width=3, color=colors[i]),
#         name=labels[i]
#     )
#     tracesList.append(trace)
# layout = go.Layout(
#     title='Genotypes Breakdown',
#     xaxis=dict(
#         title='Time [days]',
#         titlefont=dict(size=20, color='#7f7f7f')
#     ),
#     yaxis=dict(
#         title='Allele Frequency',
#         titlefont=dict(size=20, color='#7f7f7f')
#     ),
#     width=1500,
#     height=400
# )
# fig = go.Figure(data=go.Data(tracesList), layout=layout)
# py.iplot(fig,filename='stacked-area-plot-hover',validate=False)
# plotly.offline.plot(fig, filename='alleleFrequency.html')
#
#
# # Plot allele ratio dynamics ..................................................
# tracesList = []
# for i in range(0, len(labels)):
#     trace = dict(
#         x=range(0, len(inData)),
#         y=inData[:, i],
#         stackgroup='one',
#         groupnorm='fraction',
#         mode='lines',
#         line=dict(width=3, color=colors[i]),
#         name=labels[i]
#     )
#     tracesList.append(trace)
# layout = go.Layout(
#     title='Genotypes Breakdown',
#     xaxis=dict(
#         title='Time [days]',
#         titlefont=dict(size=20, color='#7f7f7f')
#     ),
#     yaxis=dict(
#         title='Allele Ratio',
#         titlefont=dict(size=20, color='#7f7f7f')
#     ),
#     width=1500,
#     height=400
# )
# fig = dict(data=tracesList, layout=layout)
# plotly.offline.plot(fig, filename='allelePercentage.html')
