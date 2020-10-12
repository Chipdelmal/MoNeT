
import re
from glob import glob


XP_NPAT = 'E_{}_{}_{}_{}_{}-{}_{}_{}.bz'


def getExperimentsIDSets(PATH_EXP, skip=-1):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids
