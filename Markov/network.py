# import networkx as nx
import numpy as np
# import random as rm
# import platform


def normalizeMskMgrMat(migrMat, clandMskMat):
    '''
    Takes the migration matrix and the masking matrix and returns the
        normalized masked migration matrix according to distance and
        point-type.
    '''
    normalized = np.empty((len(clandMskMat), len(clandMskMat)))
    mskdMigrMat = migrMat * clandMskMat
    for (i, row) in enumerate(mskdMigrMat):
        normalized[i] = row / sum(row)
    return normalized
