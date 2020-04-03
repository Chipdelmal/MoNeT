import datetime

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
(PADA, PADB, PADC) = ('*' * 79, '-' * 79, ' ' * 30)
(CRED, CYEL, CBMA, CBRE, CBBL, CWHT, CEND, CBLU, CGRE) = (
        '\033[91m', '\u001b[33m', '\u001b[35;1m',
        '\u001b[31;1m', '\u001b[34;1m', '\u001b[37m',
        '\033[0m', '\033[34m', '\033[92m'
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


def printProggress(i, xpNumb, sig):
    print(CBBL, end='\r')
    msgStr = (str(i+1).zfill(2), str(xpNumb).zfill(2), sig[i][0])
    print('- Working on ({}/{}): {}'.format(msgStr[0], msgStr[1], msgStr[2]))
    print(CEND, end='\r')
    return True


def printVideoHead(BASE_PATH, DATA_PATH, expPath, videoLocation, time):
    print(PADA)
    print('{}Generating video [{}]{}'.format(
                CWHT, str(time), CEND
            ))
    print(PADB + CRED)
    print('* PATH base: \t{}'.format(BASE_PATH))
    print('* PATH data: \t{}'.format(DATA_PATH))
    print('* PATH expr: \t{}'.format(expPath))
    print('* PATH video: \t{}'.format(videoLocation))
    print(CEND + PADB)


def printVideoTail(tStr, tEnd, console, videoLocation, cPrint=False):
    if cPrint:
        print(' '.join(console))
    print(PADB)
    print('{}Exported frames [{}]{}'.format(
                CWHT, str(tEnd - tStr), CEND
            ))
    print(CWHT, end='\r')
    print('Video saved to: ' + videoLocation)
    print(CEND, end='\r')
    print(PADA)
