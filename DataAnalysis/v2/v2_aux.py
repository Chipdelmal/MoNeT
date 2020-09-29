
import MoNeT_MGDrivE as monet


def selectPath(USR):
    if USR == 'dsk':
        PTR = '/media/hdd/WorkExperiments/mgdrive2_paper/'
    if USR == 'srv':
        PTR = '/RAID5/marshallShare/mgdrive2_paper/'
    if USR == 'per':
        PTR = './'
    # Paths to data folders
    PT_PRE = PTR + 'PREPROCESS/'
    PT_OUT = PTR + 'POSTPROCESS/'
    PT_MTR = PTR + 'SUMMARY/'
    PT_IMG = PTR + 'img/'
    fldrList = [PTR, PT_PRE, PT_OUT, PT_IMG, PT_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PTR, PT_PRE, PT_OUT, PT_IMG, PT_MTR)


def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'analyzed/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'traces/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, [i+'/' for i in expDirsTrac])
