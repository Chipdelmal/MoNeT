import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet
import driveSetupSelector as dSelect

###############################################################################
# MCR Construct
###############################################################################
BATCH=True
DRIVE=4
PROBED="E_80_00_10_50"

id, aggregationDictionary = dSelect.driveSelector(DRIVE)
type = float
path = "/Volumes/marshallShare/CLEAVR/" + id + "/ANALYZED/"
directories=monet.listDirectoriesWithPathWithinAPath(path)

style={
    "width":2, "alpha":1, "dpi":1024, "legend":True,
    "aspect":.05,
    "colors": [
        '#fc6237', '#ec0b43','#9f00cc','#94d4ff', '#232ed1',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}

if BATCH == False:
    experimentString=PROBED
    filenames = monet.readExperimentFilenames(path + experimentString)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=type
    )
    aggData = monet.aggregateGenotypesInNode(landscapeSumData, aggregationDictionary)
    fig=monet.plotMeanGenotypeTrace(aggData, style)
    plt.xlim(0,3500)
    plt.ylim(0,25000)
    plt.savefig("./images/"+ id + "/" + experimentString + "_T.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)
    # fig=monet.plotMeanGenotypeStack(aggData, style)
    # plt.xlim(0,3500)
    # plt.ylim(0,25000)
    # plt.savefig("./images/"+ id + "/" + experimentString + "_S.png",
    #             dpi=1024, facecolor='w',
    #             edgecolor='w', orientation='portrait', papertype=None,
    #             format="png", transparent=True, bbox_inches='tight',
    #             pad_inches=0, frameon=None)
    # plt.close(fig)
else:
    for i in range(0,len(directories)):
        experimentString=directories[i].split("/")[-1]
        filenames = monet.readExperimentFilenames(path + experimentString)
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=type
        )
        aggData = monet.aggregateGenotypesInNode(landscapeSumData, aggregationDictionary)
        fig=monet.plotMeanGenotypeTrace(aggData, style)
        plt.xlim(0,3500)
        plt.ylim(0,25000)
        plt.savefig("./images/"+ id + "/" + experimentString + "_T.png",
                    dpi=1024, facecolor='w',
                    edgecolor='w', orientation='portrait', papertype=None,
                    format="png", transparent=True, bbox_inches='tight',
                    pad_inches=0, frameon=None)
        plt.close(fig)
