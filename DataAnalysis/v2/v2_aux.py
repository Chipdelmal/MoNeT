
import re
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


# #############################################################################
# Count genotypes
# #############################################################################
def countGeneAppearances(genotypes, gene, pos):
    # Split genotypes
    splitGenotypes = [list(genes) for genes in genotypes]
    # Count
    appearances = []
    for p in pos:
        slot = [gene[p] for gene in splitGenotypes]
        matches = re.finditer(gene, ''.join(slot))
        appearances.extend([match.start() for match in matches])
    appearances.sort()
    return appearances


def flatten(l): return [item for sublist in l for item in sublist]


def aggregateGeneAppearances(genotypes, genes):
    gcnt = [countGeneAppearances(genotypes, gn[0], gn[1]) for gn in genes]
    return sorted(flatten(gcnt))
