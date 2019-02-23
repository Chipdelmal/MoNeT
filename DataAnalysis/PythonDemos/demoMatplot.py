import MoNeT_MGDrivE as monet

# def plotMeanGenotypeTrace(aggData, style):
#     groups = aggData['genotypes']
#     pops = aggData['population']
#     time = np.arange(len(pops))
#     df=pd.DataFrame(time , columns=['Time'])
#     final = [df[['Time']] for _ in range(len(groups))]
#     local=pd.DataFrame(pops, columns=groups)
#     fig, ax = plt.subplots()
#     ax.set_aspect(aspect=style["aspect"])
#     #plt.xticks([])
#     #plt.yticks([])
#     for j in range(len(groups)):
#         final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
#         final[j] = final[j].set_index('Time')
#     for i in range(len(final)):
#         final[i].plot(
#             ax = ax, linewidth = style["width"], legend=False,
#             color = style["colors"][i], alpha =style["alpha"]
#         )
#     legends=[]
#     for i in range(len(groups)):
#         legends.append(
#             mpatches.Patch(color=style["colors"][i], label=groups[i])
#         )
#     #plt.legend(handles=legends)
#     #ax.xaxis.set_label_text("")
#     #ax.yaxis.set_label_text("")
#     plt.ylabel("Allele Count")
#
#     return fig
#
#
# def plotMeanGenotypeStack(aggData, style):
#     groups = aggData['genotypes']
#     pops = aggData['population']
#     time = np.arange(len(pops))
#     df=pd.DataFrame(time , columns=['Time'])
#     final = [df[['Time']] for _ in range(len(groups))]
#     local=pd.DataFrame(pops, columns=groups)
#     fig, ax2 = plt.subplots()
#     ax2.set_aspect(aspect=style["aspect"])
#     allele_dict = {}
#     for j in range(len(groups)):
#         final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
#         final[j] = final[j].set_index('Time')
#     patchList=[]
#     for i in range(len(groups)):
#         patchList.append(mpatches.Patch(color=style["colors"][i], label=groups[i]))
#     for i in range(len(groups)):
#         allele_dict[groups[i]] = final[i].T.sum()
#     res = pd.DataFrame(allele_dict)
#     res.plot(kind = 'area', ax =ax2, legend=False, color=style["colors"])
#     plt.ylabel("Allele Count")
#     return fig



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

#------------------------------------------------------------------------------
# Plotting
#------------------------------------------------------------------------------
style={
    "width":2, "alpha":1,
    "dpi":1024, "legend":True,
    "aspect":.5,
    "colors": [
        '#232ed1', '#ec0b43','#9f00cc','#94d4ff', '#ec0b43',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}
fig=monet.plotMeanGenotypeTrace(aggData,style)
plt.savefig("./images/demotraces.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None)
plt.close(fig)


fig=monet.plotMeanGenotypeStack(aggData, style)
plt.savefig("./images/demostacks.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None)
plt.close(fig)

labels = aggData["genotypes"]
colors = ["rgb(25,128,255)", "rgb(255,25,128)",
          "rgb(128,0,255)", "rgb(255,0,255)"]
inData = aggData["population"]
