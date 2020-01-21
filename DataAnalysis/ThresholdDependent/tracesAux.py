import os
import aux
import numpy as np
import MoNeT_MGDrivE as monet



def setRange(ax, style):
    ax.set_xlim(style['xRange'][0], style['xRange'][1])
    ax.set_ylim(style['yRange'][0], style['yRange'][1])
    return ax


def driveGenesSelector(driveID):
    if (driveID == 'T'):
        # Translocations
        wildsList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
        homingList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
    elif (driveID == 'U'):
        # UDMel
        wildsList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
        homingList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
    elif (driveID == 'W'):
        # Wolbachia
        wildsList = [2]
        homingList = [1]
    return (wildsList, homingList)
