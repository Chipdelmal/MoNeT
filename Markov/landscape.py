import random
import numpy as np
import math
import itertools




def genURandPoint(lo, hi):
    '''
    Generates a random float number between lo and hi.
    '''
    return lo + random.random() * hi


def genURandCoord(loCoord, hiCoord):
    '''
    Generates a random (x,y) cordinate between lo and hi.
    '''
    return (genURandPoint(loCoord, hiCoord), genURandPoint(loCoord, hiCoord))


def genURandLandscape(loCoord, hiCoord, ptsNum):
    '''
    Generates a random landscape with ptsNum number of (x,y) coordinates.
    '''
    coords = [genURandCoord(loCoord, hiCoord) for _ in range(ptsNum)]
    return coords


def genUniformLandscape(loCoord, hiCoord, ptsNum):
    '''
    Generate a uniform landscape with ptsNum number of (x, y) coodinates.
    '''
    # check if ptsNum is square of an interger
    numRow = math.sqrt(ptsNum)
    if(numRow.is_integer()):
        x = np.linspace(loCoord, hiCoord, int(numRow))
        coords = list(itertools.product(x, x))
        return coords



if __name__ == "__main__":
    ptsNum = 100
    (lo, hi) = (0, 10)
    coords = genURandLandscape(lo, hi, ptsNum)
    print(coords)
