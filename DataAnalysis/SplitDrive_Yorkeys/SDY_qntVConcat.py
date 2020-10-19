
import sys
import cv2
from glob import glob
import SDY_aux as aux
import MoNeT_MGDrivE as monet


# (USR, AOI, QNT) = ('dsk', 'HLT', ['50', '75', '90'])
(USR, AOI) = (sys.argv[1], sys.argv[2])
QNT = ['50', '75', '90']
(DRV, EXP) = ('SD', 'factorial')
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
(PT_IMG_I, PT_IMG_O) = (PT_IMG + 'pstTraces/', PT_IMG + 'stacksQNT/')
monet.makeFolder(PT_IMG_O)
# Get files -------------------------------------------------------------------
imgLists = [glob(PT_IMG_I + '*HLT*' + i + '*') for i in QNT]
imgTuples = list(zip(*[sorted(i) for i in imgLists]))
# #############################################################################
# Iterate through images
# #############################################################################
for tp in imgTuples:
    fName = tp[0].split('/')[-1][:-7]
    imgArray = [cv2.imread(i) for i in tp]
    vertical = cv2.vconcat(imgArray)
    # show the output image
    cv2.imwrite(PT_IMG_O + fName + '.png', vertical)
