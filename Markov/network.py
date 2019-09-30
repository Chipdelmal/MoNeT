# import networkx as nx
import numpy as np
# import random as rm
# import platform


def normalizeMskMgrMat(migrMat, clandMskMat):
    normalized = np.empty((len(clandMskMat), len(clandMskMat)))
    mskdMigrMat = migrMat * clandMskMat
    for (i, row) in enumerate(mskdMigrMat):
        normalized[i] = row / sum(row)
    return normalized
