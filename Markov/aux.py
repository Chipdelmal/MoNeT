import numpy as np
import math as math
import vincenty as vn


def testMarkovMat(mat):
    '''
    Tests that the matrix behaves according to Markov properties (all
        rows sum to 1).
    '''
    rowMkvSums = list(map(sum, mat))
    check = [math.isclose(i, 1) for i in rowMkvSums]
    if check.count(True) == len(mat):
        return True
    return False


if __name__ == "__main__":
    print(euclideanDistance((0,0), (1, 1)))
    print(testMarkovMat(mat))
