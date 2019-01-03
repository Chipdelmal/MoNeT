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
width = 30

nx, ny = (width, width)
x = np.linspace(0, 300, nx)
y = np.linspace(0, 300, ny)
l=np.transpose(np.meshgrid(x, y))

list(itertools.chain(*l))
