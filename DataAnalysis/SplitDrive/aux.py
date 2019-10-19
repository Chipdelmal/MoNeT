import numpy as np

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
