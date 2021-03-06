import sys
import math
import numpy as np
import vincenty as vn
from scipy.stats import expon

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Distances
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def euclideanDistance(a, b):
    '''
    Should be changed for another function if we are using latlongs.
        Vincenty's formula is available in the pip package.
    '''
    dist = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return dist


def distanceMat(landscape, distFun=euclideanDistance):
    '''
    Returns the distance matrix according to the provided distance function.
        There's likely a faster implementation using list comprehension, but
        this is readable/good enough for now.
    '''
    coordsNum = len(landscape)
    distMatrix = np.empty((coordsNum, coordsNum))
    for (i, coordA) in enumerate(landscape):
        for (j, coordB) in enumerate(landscape):
            distMatrix[i][j] = distFun(coordA, coordB)
    return distMatrix
    

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Kernels
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def inverseLinearStep(distance, params=[.5, .25]):
    '''
    This function returns a migration estimate based on the inverse of the
        distance. NOTE: This is a terrible way to do it, but it's a first
        approximation. Should be replaced with the zero-inflated exponential.
    '''
    if math.isclose(distance, 0):
        return params[0]
    else:
        return (1 / params[0] * params[1])
    return True


def migrationKernel(distMat, kernelFun=inverseLinearStep, params=[.5, .25]):
    '''
    Takes in the distances matrix, zero inflated value (step) and two extra
        parameters to determine the change from distances into distance-based
        migration probabilities (based on the kernel function provided).
    '''
    coordsNum = len(distMat)
    migrMat = np.empty((coordsNum, coordsNum))
    for (i, row) in enumerate(distMat):
        for (j, dst) in enumerate(row):
            params[0] = dst
            migrMat[i][j] = kernelFun(params=params)
        # Normalize rows to sum 1
        migrMat[i] = migrMat[i] / sum(migrMat[i])
    return migrMat

def approxEqual(f1, f2):
    """
    Mirrors approxEqual function in MGDrive-Kernels.cpp
    """
    return abs(f1 - f2) <= sys.float_info.epsilon * max(abs(f1), abs(f2))

def dtruncExp(params):
    """
    Mirrors the dtruncExp truncated exponential distribution function in MGDrive-Kernels.cpp
    x the place in the support of the density function ( support of the normal is the whole real line, poisson is nonneg int )
    r is 1/scale = rate param
    a is upper truncatin bounds
    b is lower truncation bounds
    """
    x, r, a, b = params
    loc = 0
    if a >= b:
        return "argument a is greater than or equal to b"
    scale = 1.0/r
    Ga = expon.cdf(a, loc, scale)
    Gb = expon.cdf(b, loc, scale)

    if approxEqual(Ga, Gb):
        print("Truncation interval is not inside the domain of the density function")
    density = expon.pdf(x, loc, scale) / expon.cdf(b, loc, scale) - expon.cdf(a, loc, scale)
    print("density is ", density)
    return density

def zeroInflatedExponential(distMat, rate, pi):
    """
        Mirrors the zero-inflated calcHurdleExpKernel in MGDrive-Kernels.cpp
    """
    a = 1.0e-10 #lower truncation bound
    print("distMat is ",distMat)
    n = len(distMat) #num rows

    kernMat = np.zeros((n, len(distMat[1])))

    for i in range(n):
        for j in range(n):
            if i == j:
                kernMat[i][j] = 0
            else:
                kernMat[i][j] = dtruncExp(params=[distMat[i][j], rate, a, float("inf")]) #truncated density
        kernMat[i] = kernMat[i] / sum(kernMat[i]) * (1-pi) #normalize density
        kernMat[i][i] = pi #point mass at zero
    
    return kernMat

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Tests
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if __name__ == "__main__":
    landscape = ((42.3541165, -71.0693514), (40.7791472, -73.9680804))
    distMat = distanceMat(landscape, distFun=vn.vincenty)
    distMat

    row = distMat[0]

    inverseLinearStep(0, [.75, 1])

    movementProb = zeroInflatedExponential(distMat=distMat, rate=1/10, pi=0.5)

    a = 1.0e-10 #lower truncation bound
    migrationKernel(distMat, dtruncExp, params=[0, 1/10, a, float("inf")])
