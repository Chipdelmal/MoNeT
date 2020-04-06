import time
import datetime
import subprocess
import SDY_aux as aux

XP_LSTS = [
    ['E_05_10_025', 'E_05_20_025', 'E_05_30_025', 'E_15_10_025'],
    ['E_15_20_025', 'E_15_30_025', 'E_30_10_025', 'E_30_20_025'],
    ['E_30_30_025', 'E_05_10_050', 'E_05_20_050', 'E_05_30_050'],
    ['E_15_10_050', 'E_15_20_050', 'E_15_30_050', 'E_30_10_050'],
    ['E_30_20_050', 'E_30_30_050', 'E_05_10_075', 'E_05_20_075'],
    ['E_05_30_075', 'E_15_10_075', 'E_15_20_075', 'E_15_30_075'],
    ['E_30_10_075', 'E_30_20_075', 'E_30_30_075', 'E_05_10_100'],
    ['E_05_20_100', 'E_05_30_100', 'E_15_10_100', 'E_15_20_100'],
    ['E_30_30_100', 'E_15_30_100', 'E_30_10_100', 'E_30_20_100']
]

##############################################################################
# Print head
##############################################################################
(tStr, sp) = (datetime.datetime.now(), [])
print(aux.PADA)
print('{}SDY batch videos [{}]{}'.format(aux.CWHT, tStr, aux.CEND))
print(aux.PADA)
##############################################################################
# Iterate through experiments
##############################################################################
(sbLen, xpLen) = (len(XP_LSTS), len(XP_LSTS[0]))
for xpIx in range(xpLen):
    print('{}* Batch {}/{}{}'.format(aux.CRED, xpIx+1, xpLen, aux.CEND))
    for sbIx in range(sbLen):
        spLst = [
                'python', 'SDY_video.py',
                'srv', 'agg', 'hlt', XP_LSTS[sbIx][xpIx]
            ]
        print('{}* SP {}/{}: {}{}'.format(
                aux.CBMA,
                sbIx+1, sbLen, XP_LSTS[sbIx][xpIx],
                aux.CEND
            ))
        openSP = subprocess.Popen(spLst, shell=True, stderr=subprocess.STDOUT)
        sp.append(openSP)
    # time.sleep(5)
    exit_codes = [p.wait() for p in sp]
##############################################################################
# Print tail
##############################################################################
tEnd = datetime.datetime.now() - tStr
print(aux.PADA)
print('{}SDY batch videos [{}]{}'.format(aux.CWHT, str(tEnd), aux.CEND))
print(aux.PADA)
