import os
import numpy as np
import aux
import MoNeT_MGDrivE as monet

PAD = '\n' + 125 * '*' + '\n'
(CRED, CEND) = ('\033[91m', '\033[0m')
###############################################################################
# Style
###############################################################################
STYLE_HLT = {
    "width": .075, "alpha": .15, "dpi": 500,
    "legend": True, "aspect": .5, "xRange": [0,2000], "yRange": [0, 20000],
    "colors": ['#9f00cc', '#ec0b43', '#0038a8']
}
STYLE_HLT['aspect'] = monet.scaleAspect(.1, STYLE_HLT)

STYLE_ECO = {
    "width": .075, "alpha": .15, "dpi": 500,
    "legend": True, "aspect": .5, "xRange": [0,2000], "yRange": [0, 1],
    "colors": ['#ff004d', '#80ff80', '#6600ff', '#e600ff', '#b3ccff', '#333380']
}
STYLE_ECO['aspect'] = monet.scaleAspect(.1, STYLE_ECO)

###############################################################################
# Functions Definitions
###############################################################################
def normalizePopulationInNode(node, totalPopIx=-1):
    popSize = node[:,-1]
    normalizedNode = np.empty(node.shape)
    for i in range(0, len(node), 1):
        normalizedNode[i] = node[i] / popSize[i]
    return normalizedNode


def normalizeLandscapeDataRepetitions(landscapeReps, totalPopIx=-1):
    landscapes = landscapeReps['landscapes']
    for (i, land) in enumerate(landscapes):
        landscapes[i] = [normalizePopulationInNode(node, totalPopIx=totalPopIx) for node in land]
    landscapeReps['landscapes'] = landscapes
    return landscapeReps


def scaleAspect(aspect, style):
    xDiff = (style['xRange'][1] - style['xRange'][0])
    yDiff = (style['yRange'][1] - style['yRange'][0])
    return aspect * (xDiff / yDiff)


def getExperiments(PATH):
    dirs = sorted(next(os.walk(PATH))[1])
    temp = []
    for i in dirs:
        if(i != 'img'):
            temp.append(i)
    (expsNum, dirs) = (len(temp), temp)
    return (expsNum, dirs)


def makeFolder(foldername):
    if not os.path.exists(foldername):
        try:
            os.mkdir(foldername)
        except:
            raise OSError("Can't create destination directory (%s)!" % (foldername))


def selectAnalysisType(ECO, PATH_IMG):
    (PATH_HLT, PATH_ECO) = (PATH_IMG + 'hlt/', PATH_IMG + 'eco/')
    if ECO == True:
        (expType, style, path) = ('ECO', aux.STYLE_ECO, PATH_ECO)
    else:
        (expType, style, path) = ('HLT', aux.STYLE_HLT, PATH_HLT)
    return (expType, style, path)
