
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


def calcTTI(repRto, thiS):
    thiSBool = [compRatioToThreshold(repRto, i, op.lt) for i in thiS]
    ttiS = [np.argmax(thiBool == 1, axis=1) for thiBool in thiSBool]
    return ttiS


def calcTTO(repRto, thoS):
    (reps, days) = repRto.shape
    thoSBool = [compRatioToThreshold(repRto, i, op.gt) for i in thoS]
    ttoS = [np.subtract(days, np.argmin(np.flip(thoBool), axis=1)) for thoBool in thoSBool]
    return ttoS


def calcWOP(repRto, thwS):
    thwSBool = [compRatioToThreshold(repRto, i, op.lt) for i in thwS]
    wopS = [np.sum(thwBool, axis=1) for thwBool in thwSBool]
    return wopS
