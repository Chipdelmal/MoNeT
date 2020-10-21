
from glob import glob
import matplotlib
import MoNeT_MGDrivE as monet


def selectDepVars(MOI, THS, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP'):
        days = 250
        (scalers, HD_DEP) = ((1, 100, round(days)), str(THS))
    elif (MOI == 'TTI') or (MOI == 'TTO'):
        days = 750
        (scalers, HD_DEP) = ((1, 100, round(days)), str(THS))
    elif (MOI == 'RAP'):
        maxPop = 12500
        (scalers, HD_DEP) = ((1, 100, maxPop), '486')
    elif (MOI == 'MNX'):
        maxPop = 12500
        (scalers, HD_DEP) = ((1, 100, maxPop), 'min')
    # Color Mapping -----------------------------------------------------------
    if AOI == 'HLT':
        cmap = cmapC
    elif AOI == 'TRS':
        cmap = cmapM
    elif AOI == 'WLD':
        cmap = cmapW
    return (scalers, HD_DEP, cmap)


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


# #############################################################################
# Plot
# #############################################################################
def quickSaveFig(filename, fig):
    fig.savefig(
         filename,
         dpi=750, facecolor=None, edgecolor='w',
         orientation='portrait', papertype=None, format='png',
         transparent=True, bbox_inches='tight', pad_inches=.01
     )


# #############################################################################
# Color Palette
# #############################################################################
cdict = {
        'red':  ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.3, 0.3), (1.0, 0.0, 0.0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 0.25, 0.25))
    }
cmapB = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.95, 0.95)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0, 0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.4, 0.4))
    }
cmapC = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0, 0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.65, 0.65)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, .95, .95))
    }
cmapM = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.05, 0.05)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.91, 0.91)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.06, 0.06))
    }
cmapW = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)
