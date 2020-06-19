#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from glob import glob
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, title):
    print(monet.PAD)
    (cred, cwht, cend) = (monet.CRED, monet.CWHT, monet.CEND)
    print(cwht+'UCI '+title+' ['+str(time)+']'+cend)
    print(monet.PAD)
    print('{}* Root: {}{}'.format(cred, PATH_ROOT, cend))
    print('{}* Imgs: {}{}'.format(cred, PATH_IMG, cend))
    print('{}* Data: {}{}'.format(cred, PATH_DATA, cend))
    print(monet.PAD)


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'GARBAGE/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


def splitExpNames(PATH_OUT, ext='lzma'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append=''):
    figArr = monet.plotLandscapeDataRepetitions(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    # axTemp.set_xticks(range(0, STYLE["xRange"][1], 150))
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}-{}.png".format(PATH_IMG, nS, append),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')
    return True


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.lzma'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-3] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids
