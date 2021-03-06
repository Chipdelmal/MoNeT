#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

# Functions ###################################################################
def scaleAspect(aspect, style):
    xDiff = (style['xRange'][1] - style['xRange'][0])
    yDiff = (style['yRange'][1] - style['yRange'][0])
    return aspect * (xDiff / yDiff)
# Filepaths ###################################################################

(selStat, funcsID) = (0, ["SSD", "SMN", "SMD"])
pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_MINI/Experiemnts/"
pathOut = pathRoot + "images/frames/"
# Filepaths ###################################################################
(filesListMean, filesListStat) = (
    sorted(glob.glob(pathRoot + '*SMN*')),
    sorted(glob.glob(pathRoot + '*' + funcsID[selStat] + '*'))
)
filesNum = len(filesListMean)
# Style #######################################################################
colors = ["#090446", "#f20060", "#59ff00", "#ff28d4", "#6898ff", "#c6d8ff"]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleS = {
    "width": 0, "alpha": .85, "dpi": 2*512, "legend": False,
    "aspect": 1, "colors": colors, "format": "png",
    "xRange": [0, 3000],#9124],
    "yRange": [0, 45000]  # 590000]  # 2500]
}
styleS['aspect'] = scaleAspect(1, styleS)

# Main ########################################################################
for fileIx in range(len(filesListMean)):
    (fileM, fileS) = (filesListMean[fileIx], filesListStat[fileIx])
    nameID = str(filesListMean[fileIx].split('/')[-1].split('.')[-2])
    # Read Files ##############################################################
    (readDataM, readDataS) = (
            np.genfromtxt(fileM, delimiter=','),
            np.genfromtxt(fileS, delimiter=',')
        )
    # Stack ###################################################################
    data = {"genotypes": ["W", "H", "E", "R", "B"], "population": readDataM}
    fig = monet.plotMeanGenotypeStack(data, styleS)
    #ax = fig.add_subplot(111)
    #ax.set_aspect(aspect=styleS["aspect"])
    #ax.set_xlim(styleS["xRange"])
    #ax.set_ylim(styleS["yRange"])
    monet.quickSaveFigure(
        fig, pathOut + "S_" + nameID + ".png",
        format="png", dpi=styleS["dpi"]
    )
    plt.close()
    # Deviation ###############################################################
    timeRange = range(len(readDataM[0:,0]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(data["genotypes"])):
        plt.plot(
            timeRange, readDataM[0:, i],
            color=colors[i], alpha=styleS["alpha"]
        )
        max = readDataM[0:, i] + readDataS[0:, i]
        min = readDataM[0:, i] - readDataS[0:, i]
        ax.fill_between(timeRange, min, max, color=colors[i], alpha=0.1)
    ax.set_aspect(aspect=styleS["aspect"])
    ax.set_xlim(styleS["xRange"])
    ax.set_ylim(styleS["yRange"])
    monet.quickSaveFigure(
        fig, pathOut + "T_" + nameID + ".png",
        format="png", dpi=styleS["dpi"]
    )
    plt.close()


# Full traces #################################################################
timeRange = range(len(readDataM[0:,0]))
fig = plt.figure()
ax = fig.add_subplot(111)
for fileIx in range(filesNum):
    (fileM, fileS) = (filesListMean[fileIx], filesListStat[fileIx])
    nameID = fileM.split("/")[-1].split(".")[0]
    # Read Files ##############################################################
    (readDataM, readDataS) = (
            np.genfromtxt(fileM, delimiter=','),
            np.genfromtxt(fileS, delimiter=',')
        )
    for i in range(len(data["genotypes"])):
        plt.plot(
            timeRange, readDataM[0:, i],
            color=colors[i], alpha=1/(filesNum - 1) * fileIx,
            linewidth=.35#(.04 * fileIx)
        )
        # max = readDataM[0:, i] + readDataS[0:, i]
        # min = readDataM[0:, i] - readDataS[0:, i]
        # ax.fill_between(timeRange, min, max, color=colors[i], alpha=0.1)
    ax.set_aspect(aspect=styleS["aspect"])
    ax.set_xlim(styleS["xRange"])
    ax.set_ylim(styleS["yRange"])
monet.quickSaveFigure(
    fig, pathOut + "SMN_Yorkeys_AGG_1_Full.png",
    format="png", dpi=styleS["dpi"]
)

# ffmpeg -i %05d.jpg output.mp4
# ffmpeg -ss 2.6 -t 1.3 -i output.mp4 -vf fps=15,scale=320:-1:flags=lanczos,palettegen palette.png
