import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet

###############################################################################
# MCR Construct
###############################################################################

# Define the experiment's path, aggregation dictionary, and read filenames
type = float
path = "/Volumes/marshallShare/TPP/SplitDrive/ANALYZED/"
directories=monet.listDirectoriesWithPathWithinAPath(path)

style={
    "width":.1, "alpha":1,
    "dpi":1024, "legend":True,
    "aspect":.00001,#'auto',
    "colors": [
        '#fc6237', '#ec0b43','#9f00cc','#94d4ff', '#232ed1',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}

#------------------------------------------------------------------------------
# Data Handling
#------------------------------------------------------------------------------
for i in range(0,len(directories)):
    experimentString=directories[i].split("/")[-1]
    # aggregationDictionary = monet.generateAggregationDictionary(
    #     ["W", "H", "R", "B"],
    #     [
    #         [0, 0, 1, 2, 3],
    #         [1, 4, 4, 5, 6],
    #         [2, 5, 7, 7, 8],
    #         [3, 6, 8, 9, 9]
    #     ]
    # )
    filenames = monet.readExperimentFilenames(path + experimentString)

    # To analyze the sum of the whole landscape ..................................
    # Sum landscape into one array ("in place" memory-wise)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames,
        male=True,
        female=True,
        dataType=float
    )
    aggregationDictionary=monet.autoGenerateGenotypesDictionary(
        ["W","H","R","B","C"],
        landscapeSumData["genotypes"]
    )
    # Aggregate genotypes (node or landscape) ....................................
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )

    #------------------------------------------------------------------------------
    # Plotting
    #------------------------------------------------------------------------------
    # fig=monet.plotMeanGenotypeTrace(aggData,style)
    # plt.savefig("./images/"+experimentString+".png",
    #             dpi=1024, facecolor='w',
    #             edgecolor='w', orientation='portrait', papertype=None,
    #             format="png", transparent=True, bbox_inches='tight',
    #             pad_inches=0, frameon=None)
    # plt.close(fig)


    fig=monet.plotMeanGenotypeStack(aggData, style)
    plt.xlim(0,3500)
    plt.ylim(0,50000000)
    fig
    plt.savefig("./images/"+experimentString+".png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)


aggregationDictionary
