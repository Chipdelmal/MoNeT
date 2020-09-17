
import numpy as np
import operator as op
import MoNeT_MGDrivE as monet


def getPopRepsRatios(base, trace, gIx):
    (basePop, tracePops) = (base['population'], trace['landscapes'])
    ratioReps = [monet.getPopRatio(trace, basePop, gIx) for trace in tracePops]
    ratioArr = np.asarray(ratioReps)
    return ratioArr


def compRatioToThreshold(repsRatios, thld, cmprOp=op.lt):
    thresholdArray = np.apply_along_axis(cmprOp, 0, repsRatios, thld)
    return thresholdArray
