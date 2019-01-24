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
nodesNumberHalf, nodesDistance = 5, 10
for i in range(0, 9):
    tmpLine = generateCartesianLinearCoordinates()

##############################################################################
# Moore
##############################################################################
m = 4
l = 3

for b in range(1, l + 1):
    for a in range(1, l + 1):
        tagged = (m - a) + ((m - b) * m) + 1
        print(tagged)

m = 3
l = 2
for b in range(1, l + 1):
    for a in range(1, l + 1):
        tagA = (m - a) + ((m - b) * m) + 1
        tagB = (b * m) + (m + a)
        tagC = (m - a) + ((m - b) * m) + 1
        tagD = (m - a) + ((m - b) * m) + 1
        print([tagA, tagB])

##############################################################################
# Von Newmann
##############################################################################
m = 4
l = 3
for b in range(1, l + 1):
    for a in range(1, l - b + 2):
        tagged = (m - a) + ((m - b) * m) + 1
        print(tagged)
