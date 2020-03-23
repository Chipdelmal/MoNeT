import numpy as np
import aux as funcs
import SDY_select as aux
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(VOL, EXP) = ('RAID5', 'Aggregated')  # 'unAggregated'
###############################################################################
COLORS = ["#090446", "#f20060", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
STYLE = {
    "width": .1, "alpha": .15, "dpi": 2 * 300,
    "legend": True, "aspect": .5, "colors": colors,
    "xRange": [0,2000], "yRange": [0,7000]
}
PATH = '/{}/marshallShare/SplitDrive_Yorkeys/geoProof/{}'.format(VOL, EXP)
###############################################################################
if HEALTH is True:
    colors = ['#9f00cc', '#ec0b43', '#0038a8']

    pathOut = "/Volumes/marshallShare/SplitDriveSup/imgHEA/"
else:
    colors = ['#ff004d', '#80ff80', '#6600ff', '#e600ff', '#b3ccff', '#333380']
    style = {
        "width": .1, "alpha": .15, "dpi": 2 * 300,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0, 1]
    }
    pathOut = "/Volumes/marshallShare/SplitDriveSup/imgECO/"
style['aspect'] = funcs.scaleAspect(.2, style)
###############################################################################
for DRIVE in [3]:
    pathsRoot, aggregationDictionary, prepend, pathO = aux.driveSelector(
        DRIVE, HEALTH, pathRoot
    )
    pathExport = pathOut + pathO + '/'
    ###########################################################################
    print('******************************************************************')
    print('* Started Drive (' + str(DRIVE) + '/3):')
    print('*\t' + pathExport)
    print('******************************************************************')
    ###########################################################################
    pathsRoot.reverse()
    num = len(pathsRoot)
    for i in range(480, num, 1):
        pathSample = pathsRoot[i]
        experimentString = pathSample.split("/")[-1]
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                paths, aggregationDictionary,
                male=False, female=True, dataType=float
            )
        landscapeReps = funcs.normalizeLandscapeDataRepetitions(
                landscapeReps, totalPopIx=-1
            )
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
        for j in range(0, len(figsArray)):
            figsArray[j].get_axes()[0].set_xlim(0,style['xRange'][1])
            figsArray[j].get_axes()[0].set_ylim(0,style['yRange'][1])
            expOutStr = pathExport + prepend + experimentString
            monet.quickSaveFigure(
                figsArray[j], expOutStr+"_N"+str(j)+".png", dpi=style['dpi']
            )
        plt.close('all')
        print('\tExported ' + str(i + 1).rjust(4, '0') + '/' + str(num) + ': ' + expOutStr)
###############################################################################
print('******************************************************************')
print('* Finished all drives correctly')
print('******************************************************************')
