
import numpy as np
import SDY_aux as aux
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
np.seterr(divide='ignore', invalid='ignore')


###############################################################################
# Error Calculations
###############################################################################
def rpd(signal, probe):
    num = probe - signal
    den = np.abs(probe) + np.abs(signal)
    err = (num / den)   # * 2
    return np.nan_to_num(err)


###############################################################################
# Paths
###############################################################################
def getValidationExperiments(path,setName):
    base = path + setName
    names = sorted(monet.listDirectoriesInPath(base+'/ANALYZED/'))
    pthsA = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/ANALYZED/'))
    pthsB = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/GARBAGE/'))
    return (list(zip(names, pthsA, pthsB)))


def readDataPaths(aPath, gPath):
    aFiles = monet.readExperimentFilenames(aPath)
    gFiles = monet.listDirectoriesWithPathWithinAPath(gPath+'/')
    return (aFiles, gFiles)


def createFolders(foldersList):
    for fldr in foldersList:
        monet.makeFolder(fldr)


###############################################################################
# Shaping Responses
###############################################################################
def loadSummedMeanResponse(aFiles, GDICT, MALE, FEMALE):
    print(aux.CBLU, end='\r')
    print('- Loading mean response...'+aux.PADC, end='\r')
    landData = monet.loadLandscapeData(aFiles, male=MALE, female=FEMALE)
    print('- Aggregating mean response...'+aux.PADC, end='\r')
    aggDataM = monet.aggregateGenotypesInLandscape(landData, GDICT)
    aggDataM['landscape'] = sum(aggDataM['landscape'])
    print(aux.CEND, end='\r')
    return aggDataM


def loadSummedTracesResponse(gFiles, GDICT, MALE, FEMALE):
    aggDataT = monet.sumAggregatedLandscapeDataRepetitionsAlt(
        gFiles, GDICT, male=MALE, female=FEMALE
    )
    return aggDataT


def calcResponses(aFiles, gFiles, GDICT, MALE, FEMALE):
    (aggDataM, aggDataT) = (
            loadSummedMeanResponse(aFiles, GDICT, MALE, FEMALE),
            loadSummedTracesResponse(gFiles, GDICT, MALE, FEMALE)
        )
    return (aggDataM, aggDataT)


def loadAndCalcResponse(expSet, GDICT, MALE, FEMALE):
    (name, aPath, gPath) = expSet
    (aFiles, gFiles) = readDataPaths(aPath, gPath)
    (aggDtaM, aggDtaT) = calcResponses(aFiles, gFiles, GDICT, MALE, FEMALE)
    return (name, aggDtaM, aggDtaT)


###############################################################################
# Plots
###############################################################################
def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append=''):
    figArr = monet.plotLandscapeDataRepetitions(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.set_xticks(range(0, STYLE["xRange"][1], 150))
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}-{}.pdf".format(PATH_IMG, nS, append),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='pdf',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')
    return True


###############################################################################
# Videos
###############################################################################
COLORS = [
        monet.rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        monet.rescaleRGBA((0, 169, 255, 255/7.5)),    # 1: Cyan
        monet.rescaleRGBA((255, 0, 152, 255/1)),      # 2: Magenta
        monet.rescaleRGBA((37, 216, 17, 255/6)),      # 3: Bright green
        monet.rescaleRGBA((255, 255, 255, 255/1)),    # 4: White
        monet.rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]


def generateClusterGraphs(
            clstFile,
            aggList, coordinates, destination, colorList, original_corners,
            padding, dpi, countries=False, skip=False, refPopSize=1,
            verbose=True, background=False, timeLocation=(.5, .5)
        ):
    time = len(aggList[0])
    timeMax = list(range(time))
    print(destination)
    for tick in timeMax:
        imgFileName = destination+'/c_'+str(tick).zfill(6)+".png"
        if skip and os.path.isfile(imgFileName):
            continue

        for idx, cData in enumerate(aggList):
            if idx == 0:
                (fig, ax, m) = createMap(clstFile, COLORS, pad=.025)
            pops = []
            try:
                pops = cData[tick]
                alphas, size = monet.getAlphas(pops)
                if alphas:
                    monet.draw_dots(
                            m, alphas, colorList,
                            coordinates[0][idx], coordinates[1][idx],
                            size/refPopSize
                        )
                else:
                    continue
            except Exception as e:
                return e
        else:
            ax.axis('off')
            plt.text(
                    timeLocation[0], timeLocation[1], str(tick+1).zfill(4),
                    ha='left', va='top',
                    transform=fig.transFigure
                )
            fig.savefig(imgFileName,
                        dpi=dpi, orientation='portrait', papertype=None,
                        transparent=False, format="png",
                        bbox_inches='tight', pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            if original_corners:
                fig, ax, m = monet.createFig(
                        original_corners, padding, countries
                    )
            else:
                fig, ax, m = monet.createFig(coordinates, padding, countries)
        if verbose:
            print(
                    '* Exporting frame ({}/{})'.format(
                            str(tick+1).zfill(5), str(time).zfill(5)
                    ), end='\r'
                )
    return None


def createMap(clusterFile, COLORS, pad=.025):
    (minLat, maxLat, minLong, maxLong) = (0, 0, 0, 0)
    (lats, longs, clusters) = ([], [], [])
    clusterData = open(clusterFile, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (long, lat, cluster) = (
                float(tokens[1]), float(tokens[2]), int(tokens[3])
            )
        lats.append(lat)
        longs.append(long)
        clusters.append(cluster)

    (minLat, maxLat, minLong, maxLong) = (
            min(lats), max(lats), min(longs), max(longs)
        )
    (minCluster, maxCluster) = (min(clusters), max(clusters))

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, label="1")
    m = Basemap(
            projection='merc',
            llcrnrlat=minLat-pad, urcrnrlat=maxLat+pad,
            llcrnrlon=minLong-pad, urcrnrlon=maxLong+pad,
            lat_ts=20, resolution='i', ax=ax
        )
    m.drawcoastlines(color=COLORS[1], linewidth=5, zorder=-1)
    m.drawcoastlines(color=COLORS[0], linewidth=2, zorder=-1)
    m.drawcoastlines(color=COLORS[1], linewidth=.5, zorder=-1)
    # m.fillcontinents(color=COLORS[3], lake_color='aqua')
    m.scatter(
            longs, lats, latlon=True, alpha=.1, marker='x', s=1,
            cmap=plt.get_cmap('winter'), c=clusters,
            vmin=minCluster, vmax=maxCluster
        )
    ax.tick_params(
            axis='both',       # changes apply to the both
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            right=False,
            labelbottom=False,  # labels along the bottom edge are off
            labelleft=False
        )
    ax.axis('off')
    return (fig, ax, m)
