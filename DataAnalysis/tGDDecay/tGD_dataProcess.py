import numpy as np
import pandas as pd
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


def calcTTI(repRto, thiS, clipValue=None):
    if clipValue is None:
        (_, days) = repRto.shape
    else:
        days = clipValue
    thiSBool = [compRatioToThreshold(repRto, i, op.lt) for i in thiS]
    ttiS = [np.argmax(thiBool == 1, axis=1) for thiBool in thiSBool]
    clipped = [[x if x > 0 else days for x in i] for i in ttiS]
    return clipped


def calcTTO(repRto, thoS):
    (reps, days) = repRto.shape
    thoSBool = [compRatioToThreshold(repRto, i, op.gt) for i in thoS]
    ttoS = [np.subtract(days, np.argmin(np.flip(thoBool), axis=1)) for thoBool in thoSBool]
    return ttoS


def calcWOP(repRto, thwS):
    thwSBool = [compRatioToThreshold(repRto, i, op.lt) for i in thwS]
    wopS = [np.sum(thwBool, axis=1) for thwBool in thwSBool]
    return wopS


def calcMinMax(repRto):
    (mni, mxi) = (repRto.min(axis=1), repRto.max(axis=1))
    mnx = np.asarray([np.where(repRto[i] == mni[i])[0][0] for i in range(len(mni))])
    mxx = np.asarray([np.where(repRto[i] == mxi[i])[0][0] for i in range(len(mxi))])
    return ((mni, mnx), (mxi, mxx))


def getRatioAtTime(repRto, ttpS):
    return np.asarray([repRto[:, ttp] for ttp in ttpS])


def initEmptyDFs(
            fPaths, header, thiS, thoS, thwS, ttpS,
            peak=['min', 'minx', 'max', 'maxx']
        ):
    fNum = len(fPaths)
    heads = [(header+i) for i in (thiS, thoS, thwS, ttpS, peak)]
    DFEmpty = [pd.DataFrame(int(0), index=range(fNum), columns=h) for h in heads]
    return DFEmpty


def filterDFWithID(df, xpid):
    xpidz = list(zip(list(df.columns)[:7], xpid))
    filters = [df[i[0]] == i[1] for i in xpidz]
    filter = list(map(all, zip(*filters)))
    return df[filter]
