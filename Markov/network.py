import networkx as nx
import numpy as np
import random as rm


if __name__ == "__main__":
    # n: Nodes
    # nt: Nodes types
    (nNum, ntNum) = (10, 3)
    (tol, passMkvTest) = (.99, True)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Define the classes masking vector
    #   By default, mosquitos will shift to the next state (node type)
    #   with 100% probability
    mskVct = np.zeros(ntNum)
    mskVct[1] = 1

    # Check Markovian property
    if np.sum(mskVct) < tol:
        passMkvTest = False
        print("The mask vector is not Markovian")

    # Create the mask matrix
    mskMat = np.empty((ntNum, ntNum))
    mskMat[0] = np.array([0,0,0])
    mskMat

    for i in range(ntNum):
        print(np.roll(mskVct, i))
    mskMat

    mksMat

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Define an adjacency matrix manually
     mat = np.matrix([
            [0.2, 0.6, 0.2],
            [0.1, 0.6, 0.3],
            [0.2, 0.7, 0.1]
        ])

    # Check Markovian property
    if map(np.sum, mat) < tol:
        passMkvTest = False
        print("The transitions matrix is not Markovian")
