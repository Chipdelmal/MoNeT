
from glob import glob
import MoNeT_MGDrivE as monet


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Yorkeys/{}/'.format(EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/media/hdd/WorkExperiments/SDY/{}/'.format(EXP)
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/SDY/{}/'.format(EXP)
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'TRACE/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def getZeroFilteredFiles(PT_PRE, AOI, FZ=False, tyTag=('sum', 'srp')):
    if FZ:
        fLists = list(zip(*[getFilteredFiles(
                PT_PRE+'*_00_*'+AOI+'*'+tp+'*',
                PT_PRE+'*'+AOI+'*'+tp+'*') for tp in tyTag]
            ))
    else:
        fLists = list(zip(
                *[sorted(glob(PT_PRE+'*'+AOI+'*'+tp+'*')) for tp in tyTag]
            ))
    return fLists


# #############################################################################
# Filtered lists
# #############################################################################
def getFilteredFiles(filterGlobPattern, unfilteredGlobPattern):
    filterSet = set(glob(filterGlobPattern))
    fullSet = set(glob(unfilteredGlobPattern))
    filteredList = sorted(list(fullSet - filterSet))
    return filteredList


# #############################################################################
# Terminal
# #############################################################################
def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, title):
    print(monet.PAD)
    (cred, cwht, cend) = (monet.CRED, monet.CWHT, monet.CEND)
    print(cwht+'MoNeT: '+title+' ['+str(time)+']'+cend)
    print(monet.PAD)
    print('{}* Root: {}{}'.format(cred, PATH_ROOT, cend))
    print('{}* Imgs: {}{}'.format(cred, PATH_IMG, cend))
    print('{}* Data: {}{}'.format(cred, PATH_DATA, cend))
    print(monet.PAD)
