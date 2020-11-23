
import sys
import cv2
from glob import glob
import tGD_aux as aux
from datetime import datetime
import MoNeT_MGDrivE as monet


# (USR, DRV, QNT) = ('dsk', 'tGD', '50')
(USR, DRV, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3])
AOI = ['HLT', 'TRS', 'WLD']
if (USR == 'srv2') or (USR == 'dsk'):
    EXPS = ('000', )
    NOI = [[0]]
else:
    EXPS = ('050', '100', '400', '800')
    NOI = [[0], [1]]
for EXP in EXPS:
    # #############################################################################
    # Setup paths and drive
    # #############################################################################
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, EXP)
    (PT_IMG_I, PT_IMG_O) = (PT_IMG + 'pstTraces/', PT_IMG + 'stacksAOI/')
    monet.makeFolder(PT_IMG_O)
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG_I, PT_IMG_O, tS, 'AOI VConcat ' + QNT)
    # Get files -------------------------------------------------------------------
    imgLists = [glob('{}*{}*{}*'.format(PT_IMG_I, i, QNT)) for i in AOI]
    imgTuples = list(zip(*[sorted(i) for i in imgLists]))
    # #############################################################################
    # Iterate through images
    # #############################################################################
    fmt = 'Processing {}/' + str(len(imgTuples))
    for (i, tp) in enumerate(imgTuples):
        print(fmt.format(str(i + 1).zfill(3)), end='\r')
        fName = tp[0].split('/')[-1][:-4].replace('-HLT_', '-')
        imgArray = [cv2.imread(i) for i in tp]
        vertical = cv2.hconcat(imgArray)
        # show the output image
        cv2.imwrite(PT_IMG_O + fName + '.png', vertical)
