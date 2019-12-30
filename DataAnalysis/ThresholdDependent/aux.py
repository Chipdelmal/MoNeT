import math


def roundup(x):
    return int(math.ceil(x / 10000.0)) * 10000


def getFilenameFromPath(path):
    return path.split('/')[-1].split('.')[0]


def introgrationDay(aggData, geneIx, threshold, skipDays=10, refFrame=-1):
    popCounts = aggData['population']
    for j in range(len(popCounts)):
        totalPop = sum(popCounts[j])
        if (totalPop > 0):
            ratio = popCounts[j][geneIx] / sum(popCounts[-1])
            if (ratio <= threshold):
                return j
    return 0
