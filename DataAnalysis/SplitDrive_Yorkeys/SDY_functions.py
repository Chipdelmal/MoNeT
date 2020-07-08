
import os
import operator as op
import numpy as np
from glob import glob
import SDY_aux as aux
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
np.seterr(divide='ignore', invalid='ignore')


###############################################################################
# Pops Thresholds
###############################################################################
def comparePopToThresholds(ratioOI, thresholds, cmprOp=op.lt):
    flagsArray = np.empty((len(ratioOI), len(thresholds)), dtype=bool)
    for (i, dayData) in enumerate(ratioOI):
        closeFlags = [cmprOp(dayData, i) for i in thresholds]
        flagsArray[i] = closeFlags
    return flagsArray


def getPopRatio(prbPop, refPop, gIx):
    (a, b) = (prbPop, refPop)
    ratio = np.divide(a, b, out=np.zeros_like(a), where=b != 0)
    ratioOI = [row[gIx] for row in ratio]
    return ratioOI


def trueIndices(boolList):
    trueIx = [i for (i, x) in enumerate(boolList) if x == 1]
    if len(trueIx) > 0:
        return trueIx
    else:
        return [np.nan]


def thresholdMet(thsArray):
    thsNum = len(thsArray[0])
    thrsMet = [None] * thsNum
    for col in range(thsNum):
        boolCol = [i[col] for i in thsArray]
        daysAbove = trueIndices(boolCol)
        thrsMet[col] = daysAbove
    return thrsMet


def calcMeanTTI(meanPrb, meanRef, thresholds, gIx):
    ratioOI = getPopRatio(meanPrb['population'], meanRef['population'], gIx)
    thsArray = comparePopToThresholds(ratioOI, thresholds)
    thsDays = thresholdMet(thsArray)
    ttiAn = [i[0] for i in thsDays]
    return ttiAn


def calcQuantTTI(srpPrb, meanRef, thresholds, gIx, quantile=.95):
    prb = srpPrb['landscapes']
    smpNum = len(prb)
    ttiArr = np.empty((smpNum, len(thresholds)))
    for s in range(smpNum):
        refPop = meanRef['population']
        ratioOI = getPopRatio(prb[s], refPop, gIx)
        thsArray = comparePopToThresholds(ratioOI, thresholds)
        thsDays = thresholdMet(thsArray)
        ttiArr[s] = [i[0] for i in thsDays]
    quant = np.nanquantile(ttiArr, quantile, axis=0)
    return quant

###############################################################################
# PreProcessed
###############################################################################
def getPreProcessedExperiments(path, type, ext='.lzma'):
    files = sorted(glob(path + '*' + type + ext))
    names = [st.split('/')[-1].split('.')[-2][:-4] for st in files]
    return list(zip(names, files))


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
def getValidationExperiments(path, setName):
    base = path + setName
    names = sorted(monet.listDirectoriesInPath(base+'/ANALYZED/'))
    pthsA = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/ANALYZED/'))
    pthsB = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/GARBAGE/'))
    return (list(zip(names, pthsA, pthsB)))


def readDataPaths(aPath, gPath):
    aFiles = monet.readExperimentFilenames(aPath)
    gFiles = monet.listDirectoriesWithPathWithinAPath(gPath+'/')
    return (aFiles, gFiles)


# def createFolders(foldersList):
#     for fldr in foldersList:
#         monet.makeFolder(fldr)


###############################################################################
# Shaping Responses
###############################################################################
def loadSummedMeanResponse(aFiles, GDICT, MALE, FEMALE):
    print(aux.CBLU, end='\r')
    # print('\t Loading mean response...'+aux.PADC, end='\r')
    landData = monet.loadLandscapeData(aFiles, male=MALE, female=FEMALE)
    # print('\t Aggregating mean response...'+aux.PADC, end='\r')
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
    axTemp.axhline(y=50000, linewidth=.25, ls='dashed',  color=(0,0,0,.25))
    axTemp.axhline(y=100000, linewidth=.25, ls='dashed', color=(0,0,0,.25))
    figArr[0].savefig(
            "{}/{}-{}.png".format(PATH_IMG, nS, append),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
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


def createFig(coordinates, padding, countries):
    fig = None
    ax = None
    m = None
    minLat = min(coordinates[0])
    maxLat = max(coordinates[0])
    minLong = min(coordinates[1])
    maxLong = max(coordinates[1])
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.tick_params(
            axis='both',          # changes apply to the both
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            right=False,
            labelbottom=False,  # labels along the bottom edge are off
            labelleft=False
        )
    m = Basemap(
            projection='merc',
            llcrnrlat=minLat-padding, urcrnrlat=maxLat+padding,
            llcrnrlon=minLong-padding, urcrnrlon=maxLong+padding, lat_ts=20,
            resolution='i', ax=ax
        )
    m.drawcounties(linewidth=0.3)
    if countries:
        m.drawcoastlines(linewidth=0.3)
        m.drawcountries(linewidth=0.3)
    return (fig, ax, m)


def generateClusterGraphs(
            clstFile,
            aggList, coordinates, destination, colorList, original_corners,
            padding, dpi, countries=False, skip=False, refPopSize=1,
            verbose=True, background=False, timeLocation=(.5, .5)
        ):
    time = len(aggList[0])
    timeMax = list(range(time))
    for tick in timeMax:
        imgFileName = destination+'/c_'+str(tick).zfill(6)+".png"
        if skip and os.path.isfile(imgFileName):
            continue

        for (idx, cData) in enumerate(aggList):
            if idx == 0:
                (fig, ax, m) = createMap(clstFile, COLORS, pad=padding)
            pops = []
            try:
                pops = cData[tick]
                alphas, size = monet.getAlphas(pops)
                if alphas:
                    draw_dots(
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
                fig, ax, m = createFig(original_corners, padding, countries)
            else:
                fig, ax, m = createFig(coordinates, padding, countries)
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
    # m.drawcoastlines(color=COLORS[1], linewidth=5, zorder=-1)
    # m.drawcoastlines(color=COLORS[0], linewidth=2, zorder=-1)
    # m.drawcoastlines(color=COLORS[1], linewidth=.5, zorder=-1)
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


def draw_dots(m, alphas, colorList, long=0, lat=0, size=60):
    for idx, value in enumerate(alphas):
        m.scatter(
                [long], [lat], latlon=True, marker=(6, 0),
                s=max(10, 0.11 * size), facecolor=colorList[idx],
                alpha=value, linewidths=.25, edgecolors='White'
            )
    return m


###############################################################################
# New
###############################################################################
def splitExpNames(PATH_OUT):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.lzma')]
    return sorted(list(set(out)))


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'GARBAGE/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


def printExpTerminal(time, PATH_ROOT, PATH_IMG, PATH_DATA):
    print(aux.PADA)
    printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, str(time))
    expOutRootPath = PATH_IMG
    print(aux.PADA)
    monet.makeFolder(expOutRootPath)


def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time):
    print(
            aux.CWHT + 'SDY Experiments Analysis '
            + '[' + time + ']' + aux.CEND
        )
    print(aux.PADB)
    print(aux.CRED + '* Root  PATH: ' + PATH_ROOT + aux.CEND)
    print(aux.CRED + '* Data  PATH: ' + PATH_DATA + aux.CEND)
    print(aux.CRED + '* Image PATH: ' + PATH_IMG + aux.CEND)


def lenAndDigits(collection):
    """Returns the length of a list and the number of digits for z-padding
    Args:
        collection (list): Collection of elements with the "len" method
            implemented.
    Returns:
        tuple: (number of elements in the collection, required digits)
    """
    length = len(collection)
    digs = len(str(length))
    return (length, digs)
