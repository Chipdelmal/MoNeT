
import numpy as np
import tGD_aux as aux
import tGD_plots as plots
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


def getAggDataSSDay(pathsRoot, i, aggregationDictionary):
    pathSample = pathsRoot[i] + "/"
    experimentString = pathSample.split("/")[-2]
    filenames = monet.readExperimentFilenames(pathSample)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )
    ssDay = aux.reachedSteadtStateAtDay(aggData, .01)
    return aggData, ssDay, experimentString


def getLandscapeReps(i, pathRoot, pathExt, aggregationDictionary):
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
            pathRoot + pathExt + "ANALYZED/"
        )
    aggData, ssDay, _ = getAggDataSSDay(pathsRoot, i, aggregationDictionary)
    ssDay = 0
    #######################################################################
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    pathSample = pathsRoot[i]
    experimentString = pathSample.split("/")[-1]
    paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
    landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, aggregationDictionary,
        male=False, female=True, dataType=float
    )
    return landscapeReps, ssDay, experimentString


def plotAndSaveLandscapeReps(
            landscapeReps, ssDay, path, xRange, yRangeFixed, style
        ):
    figsArray = plots.plotLandscapeDataRepetitions(
            landscapeReps,
            style,
            ssDay,
            yRangeFixed
        )
    for i in range(0, len(figsArray)):
        figsArray[i].get_axes()[0].set_xlim(0, xRange)
        figsArray[i].get_axes()[0].set_ylim(0, yRangeFixed)
        figsArray[i].get_axes()[0].set_aspect(.01)
        monet.quickSaveFigure(
            figsArray[i],
            path,
            dpi=750,
            format="pdf"
        )
        plt.close()


def adjustAggDataForDrive(aggData, DRIVE):
    if not (DRIVE == 1 or DRIVE == 2):
        aggData = {
            "genotypes": aggData["genotypes"],
            "population": aggData["population"]/2
        }
    return aggData


def plotAndSaveStack(
            aggData, ssDay, ffString, ffStringH, path, xRange, yRange, styleS
        ):
    figB = plots.plotMeanGenotypeStack(aggData, styleS, ssDay, 2 * yRange)
    figB.get_axes()[0].set_xlim(0, xRange)
    figB.get_axes()[0].set_ylim(0, 2 * yRange)
    #figB.get_axes()[0].set_title(
    #    "[tSS: "+str(ssDay)+"] :: ["+ffString+"] :: ["+ffStringH + "]",
    #    fontsize=5
    #)
    monet.quickSaveFigure(
        figB,
        path,
        dpi=1024,
        format="pdf"
    )
    plt.close()


def getTimeToMin(aggData):
    pop = [sum(row) for row in aggData['population']]
    for time in range(len(pop)):
        popMin = min(pop)
        if np.isclose(pop[time], popMin, atol=.1):
            break
    return (time, popMin)


def quickSaveFigure(
    fig,
    path,
    dpi=1024,
    format=None
):
    fig.savefig(
        path, facecolor='w',
        edgecolor='w', orientation='portrait',
        transparent=True, bbox_inches=None,
        pad_inches=0, frameon=None
    )


def getFFStrings(aggData, DRIVE):
    if (DRIVE == 1 or DRIVE == 2):
        groupingsList = [[2]]
        groupingsListH = [[1]]
        ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
        ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
        ffString = "p(R): " + format(ratiosAtEnd[0], '.3f')
        ffStringH = "p(H): " + format(ratiosAtEndH[0], '.3f')
    else:
        groupingsList = [[2], [3], [2, 3]]
        groupingsListH = [[1], [4], [1, 4]]
        ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
        ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
        intersection = 4 * (ratiosAtEnd[0] * ratiosAtEnd[1])
        intersectionH = 4 * (ratiosAtEndH[0] * ratiosAtEndH[1])
        union = 2*ratiosAtEnd[0] + 2*ratiosAtEnd[1] - 4*(ratiosAtEnd[0] * ratiosAtEnd[1])
        unionH = 2*ratiosAtEndH[0] + 2*ratiosAtEndH[1] - 4*(ratiosAtEndH[0] * ratiosAtEndH[1])
        ffString = "p(R1): " + format(ratiosAtEnd[0]*2, '.3f') + ", p(R2): " + format(
            ratiosAtEnd[1]*2, '.3f') + ", p(R1&R2): " + format(intersection,
            '.3f') + ", p(R1|R2): " + format(union, '.3f')
        ffStringH = "p(H): " + format(ratiosAtEndH[0]*2, '.3f') + ", p(G): " + format(
            ratiosAtEndH[1]*2, '.3f') + ", p(H&G): " + format(intersectionH,
            '.3f') + ", p(H|G): " + format(unionH, '.3f')
    return ffString, ffStringH
