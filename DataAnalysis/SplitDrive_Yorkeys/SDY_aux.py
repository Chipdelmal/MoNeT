import MoNeT_MGDrivE as monet

###############################################################################
# Genotypes Selection
###############################################################################
GENES = ['W', 'H', 'R', 'B', 'C']
GENOTYPES = [
        'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR',
        'WWRB', 'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR',
        'WCHB', 'WCRR', 'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB',
        'CCHH', 'CCHR', 'CCHB', 'CCRR', 'CCRB', 'CCBB'
    ]

###############################################################################
# Terminal
###############################################################################
(PADA, PADB) = ('*' * 79, '-' * 79)
(CRED, CYEL, CBMA, CBRE, CBBL, CWHT, CEND) = (
        '\033[91m', '\u001b[33m', '\u001b[35;1m',
        '\u001b[31;1m', '\u001b[34;1m', '\u001b[37m',
        '\033[0m'
    )


def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, name):
    print(PADA)
    print(
            CWHT + 'Split Drive: ' + name
            + '[' + time + ']' + CEND
        )
    print(PADB)
    print(CRED + '* Root  PATH: ' + PATH_ROOT + CEND)
    print(CRED + '* Data  PATH: ' + PATH_DATA + CEND)
    print(CRED + '* Image PATH: ' + PATH_IMG + CEND)
    print(PADA)


def printExperimentTail(time, name):
    print(PADA)
    print(
            CWHT + 'Split Drive: ' + name
            + '[' + time + ']' + CEND
        )
    print(PADA)


def getValidationExperiments(path,setName):
    base = path + setName
    names = sorted(monet.listDirectoriesInPath(base+'/ANALYZED/'))
    pthsA = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/ANALYZED/'))
    pthsB = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/GARBAGE/'))
    return (list(zip(names, pthsA, pthsB)))
