import numpy as np
import itertools


def generateCartesianLinearCoordinates(
    nodesNumberHalf,
    nodesDistance,
    xStart=0,
    yConstant=0
):
    xCoords = np.linspace(
        xStart,
        nodesDistance * nodesNumberHalf * 2,
        nodesNumberHalf * 2
    )
    yCoords = [yConstant] * nodesNumberHalf * 2
    xyCoords = np.transpose(np.array([xCoords, yCoords]))
    return(xyCoords)

##############################################################################
# Line
generateCartesianLinearCoordinates(5, 10, xStart=0, yConstant=10)

##############################################################################
# Rectangle
nodesNumberHalf, nodesDistance = 5,10
for i in range(0,9):
    tmpLine = generateCartesianLinearCoordinates()
