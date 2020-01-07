import sys
import aux as aux
import drive as drive
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


###############################################################################
# Code for terminal-call: python main.py "srv" "eco"
###############################################################################
if sys.argv[1] != "srv":
    (ECO, ROOT_PTH) = (sys.argv[2] == 'eco', '/Volumes/')
else:
    (ECO, ROOT_PTH) = (sys.argv[2] == 'eco', '/RAID5/')
PATH = '/' + ROOT_PTH + '/marshallShare/SplitDriveSup/'
# For testing #################################################################
(ECO, PATH) = (False, '/Volumes/marshallShare/SplitDriveSup/')
###############################################################################
# Setup paths and analysis type
###############################################################################
PATH_IMG = PATH + 'img/'
folders = [
        'SplitDrive'
        # 'ylinkedXShredder', 'autosomalXShredder',
        # 'IIT', 'SIT', 'fsRIDL', 'pgSIT', 'CRISPR'
    ]
(expType, style, path, doi) = aux.selectAnalysisType(ECO, PATH_IMG)
(NOI, thresholds, SSPOP) = (0, [.9, .75, .5, .25, .1], 10000)
###############################################################################
# Iterate through folders
###############################################################################
dir = folders[0]
for dir in folders:
    # Get drive parameters
    drivePars = drive.driveSelector(dir)
    ###########################################################################
    # Paths
    ###########################################################################
    (pathDrive, pathDriveM) = (
        PATH + drivePars.get('folder') + '/GARBAGE/',
        PATH + drivePars.get('folder') + '/ANALYZED/'
    )
    (pathExps, pathExpsM) = (
        monet.listDirectoriesWithPathWithinAPath(pathDrive),
        monet.listDirectoriesWithPathWithinAPath(pathDriveM)
    )
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    time = str(datetime.datetime.now())
    print(aux.CRED + '\n\nE: ' + drivePars.get('folder') + aux.CEND)
    print(aux.CRED + 'O: ' + path + dir + aux.CEND)
    print(aux.PAD + '* Processing Experiments [{0}]'.format(time) + aux.PAD)
    ###########################################################################
    monet.makeFolder(path + dir)
    (num, drv) = (len(pathExps), drivePars.get(expType))
    for i in range(4, 6, 1):
        (pathSample, pathSampleM) = (pathExps[i], pathExpsM[i])
        experimentString = pathSample.split("/")[-1]
        #######################################################################
        # Mean response analysis
        #   Calculates the times for drives to achieve given thresholds of
        #   interest (for vertical lines in traces).
        #######################################################################
        # Load files with the mean response and aggregate #####################
        gIx = drivePars['HLT']['genotypes'].index('Other')
        filenames = monet.readExperimentFilenames(pathSampleM)
        landscapeData = monet.loadLandscapeData(
                filenames, male=True, female=True, dataType=float
            )
        aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                landscapeData, drivePars.get('HLT')
            )
        # Get the crosses through thresholds ##################################
        nodePop = aggregatedNodesData['landscape'][NOI]
        thrsBool = monet.comparePopToThresholds(
                nodePop, gIx, [0, 1], thresholds, refPop=SSPOP
            )
        # Get the info to min pop #############################################
        nodePopDict = {}
        nodePopDict["population"] = nodePop
        minTuple = aux.getTimeToMinAtAllele(nodePopDict, gIx)
        # Calculate the metrics ###############################################
        (chngDays, prtcDays) = (
                monet.getConditionChangeDays(thrsBool),
                monet.countConditionDays(thrsBool)
            )
        #######################################################################
        # Traces
        #   Generates the plot of the experiment at a repetition level.
        #######################################################################
        # Load Data ###########################################################
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                paths, drv, male=True, female=True
            )
        if(ECO):
            landscapeReps = monet.normalizeLandscapeDataRepetitions(
                    landscapeReps, lociiScaler=drivePars['loc']
                )
        # Plot ################################################################
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
        for j in range(0, len(figsArray)):
            title = aux.parseTitle(thresholds, prtcDays)
            minTitle = aux.parseMinTitle(minTuple)
            axTemp = figsArray[j].get_axes()[0]
            axTemp = aux.setRange(axTemp, style)
            axTemp = aux.printTitle(axTemp, title)
            axTemp = aux.printMinTitle(axTemp, minTitle)
            axTemp = aux.printVLines(axTemp, chngDays)
            axTemp = aux.printMinLines(axTemp, minTuple, style)
            expOutStr = path + drivePars.get('folder') + '/' + experimentString
            monet.quickSaveFigure(
                    figsArray[j], expOutStr + "_N" + str(j) + ".png",
                    dpi=style['dpi']
                )
        plt.close('all')
        # Terminal ############################################################
        print(
                'Exported {0}/{1}: {2}'.format(
                        str(i+1).rjust(4, '0'), num, expOutStr
                    )
            )
    ##########################################################################
    # Export color palette
    ##########################################################################
    # drvNum = len(drv['genotypes'])
    # (labels, colors) = (drv['genotypes'], style['colors'][0:drvNum])
    # filename = path + drivePars.get('folder') + '/legend.png'
    # monet.exportGeneLegend(labels, colors, filename, dpi=750)
##############################################################################
time = str(datetime.datetime.now())
print(aux.PAD + '* Finished [{0}]'.format(time) + aux.PAD)
##############################################################################
