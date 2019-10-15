import random
import numpy as np


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


if __name__ == "__main__":
    ptsNum = 100
    (lo, hi) = (0, 10)
    coords = genURandLandscape(lo, hi, ptsNum)
    print(coords)
