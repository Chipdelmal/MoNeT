import math
import numpy as np
import landscape as land
import network as mntw
from random import choices


def calcClandMskMat(pointClasses, mskMat):
    '''
    Calculates the masking matrix that corresponds to the type of the point
        (bout) in the landscape.
    '''
    ptsNum = len(pointClasses)
    clandMskMat = np.empty((ptsNum, ptsNum))
    for i in range(ptsNum):
        currentClass = pointClasses[i]
        currentMsk = mskMat[currentClass]
        clandMskMat[i] = [currentMsk[j] for j in pointClasses]
    return clandMskMat


def genURandLandscapeClasses(classesNumber, ptsNum):
    '''
    Generates the vector that defines the classes of the points in the
        landscape.
    '''
    return np.random.randint(classesNumber, size=ptsNum)

ptsNum=10
probability = [0.7, 0.2, 0.1]
classesNumber = 3

def genMRandLanscapeClasses(classesNumber, ptsNum, probability):
    '''
    Generates the vector that defines the classes of the points
    based on the probability vector (multinomial distribution)
    '''
    # check if the probability vector is valid
    if all( p>= 0 and p <=1 for p in probability) and \
    math.isclose(sum(probability), 1.0, rel_tol=1e-5):
        return np.random.choice(classesNumber, ptsNum, p=probability)


def genMskMat(ntNum=2, vct=[0, 1], tol=.99):
    '''
    This function creates the masking matrix that defines how probable is for
        mosquitos to transition from one state to the next. This assumes the
        change from one state to the next is uniformly probable (mosquitos
        spend the same amount of time in each phase). For a more complicated
        scenario, the matrix should be manually generated.
    '''
    # Make sure the input vector is Markovian
    if np.sum(vct) < tol:
        print("Masking vector is not Markovian {0}".format(str(np.sum(vct))))
        return None
    # Generate the mask matrix if the number of classes is equal to the length
    #   to the masking vector.
    if len(vct) != ntNum:
        print('''Number of node types ({1}) should be equal to mask
        vector length ({2}).'''.format(str(ntNum), str(len(vct))))
        return None
    else:
        mskVct = vct
    # Create the mask matrix
    mskMat = np.empty((ntNum, ntNum))
    for i in range(ntNum):
        mskMat[i] = np.roll(mskVct, i)
    return mskMat


if __name__ == "__main__":
    # n: Nodes
    # nt: Nodes types
    (nNum, mskVct) = (3, [0, .75, .25])
    (tol, passMkvTest) = (.99, True)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Define the classes masking matrix
    mskMat = genMskMat(nNum, mskVct)
    print(mskMat)
    # Check Markovian property
    if np.sum(mskMat) < nNum * tol:
        passMkvTest = False
        print("The transitions matrix is not Markovian")

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Define an adjacency matrix manually
    mat = np.matrix([
            [0.2, 0.6, 0.2],
            [0.1, 0.6, 0.3],
            [0.2, 0.7, 0.1]
        ])
