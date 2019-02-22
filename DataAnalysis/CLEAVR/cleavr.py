import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet
import auxiliaryFunctions as aux

###############################################################################
# Select experiment & output setup
###############################################################################
BATCH=False
DRIVE=1
EXPORT_TO_DRIVE=False
PROBED="E_100_00_10_50"
# Key: E_(Cutting rate)_(H allele cost)_(releases)_(mosquitoes per release)
###############################################################################
# Setup variables
###############################################################################
id, aggregationDictionary = aux.driveSelector(DRIVE)
path = "/Volumes/marshallShare/CLEAVR/"+id+"/ANALYZED/"
if EXPORT_TO_DRIVE:
    output = "/Volumes/marshallShare/CLEAVR/"+id+"/images/"
else:
    output = "./images/"+id+"/"
directories=monet.listDirectoriesWithPathWithinAPath(path)
# Style .......................................................................
if (DRIVE == 1) or (DRIVE == 2):
    aspect, yrange = [.25, 2*25000]
elif (DRIVE == 3) or (DRIVE == 4):
    aspect, yrange = [.5, 25000]
style={
    "width":2, "alpha":1, "dpi":1024, "legend":True,
    "aspect":.025, "colors": [
        '#9f00cc', '#ec0b43','#ff009d','#94d4ff', '#232ed1',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}
###############################################################################
# Run Routine
###############################################################################
if BATCH == False:
    experimentString=PROBED
    aggData=aux.aggregateDataFromPath(path+experimentString,aggregationDictionary)
    fig=monet.plotMeanGenotypeTrace(aggData, style)
    plt.xlim(0,3600)
    plt.ylim(0,yrange)
    plt.savefig(output + experimentString + "_T.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)
    fig=monet.plotMeanGenotypeStack(aggData, style)
    plt.xlim(0,3500)
    plt.ylim(0,yrange)
    plt.savefig(output + experimentString + "_S.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)
else:
    for i in range(0,len(directories)):
        experimentString=directories[i].split("/")[-1]
        aggData = aux.aggregateDataFromPath(path+experimentString,aggregationDictionary)
        fig=monet.plotMeanGenotypeTrace(aggData, style)
        plt.xlim(0,3600)
        plt.ylim(0,yrange)
        plt.savefig(output + experimentString + "_T.png",
                    dpi=500, facecolor='w',
                    edgecolor='w', orientation='portrait', papertype=None,
                    format="png", transparent=True, bbox_inches='tight',
                    pad_inches=0, frameon=None)
        plt.close(fig)
