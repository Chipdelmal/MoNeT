#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import uciPan_fun as fun
import uciPan_aux as aux
# import uciPan_drive as drv
# import uciSTP_indices as ix
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

(USR, XPM, LAND, SET) = ('dsk', sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, XPM, LAND, SET) = ('dsk', 'Tomas', 'tParams', 'kernel_1')
# (USR, XPM, LAND, SET) = ('dsk', 'Panmictic', 'tParams', 'island')
(DRIVE_ID, STP, SKP, FMT) = ('LDR', True, False, '.lzma')
(thr, REL_STRT, WRM, QNT) = ([.05, .50], 0, 0, .95)
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/{}/{}/{}/'.format(XPM, LAND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/{}/{}/{}/'.format(XPM, LAND, SET)
# Setting paths
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
PATH_OUT = PATH_DATA + 'PREPROCESS/'
# Print terminal info and create folder
tS = datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
print(monet.PADL)
###############################################################################
#
###############################################################################
# Colors
(CLR, CMAPS) = (aux.colorsH, aux.cmapsH)
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .5,
        "colors": CLR, "xRange": [0, 1825], "yRange": [0, 10 * 100000]
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'rep')
fLists = list(zip(*[sorted(glob(PATH_OUT+'*'+tp+FMT)) for tp in tyTag]))
rLists = list(zip(*[sorted(glob(PATH_OUT+'*_00_*-*'+tp+FMT)) for tp in tyTag]))
print(rLists)
###############################################################################
# Process files
###############################################################################
# (xpNum, digs) = fun.lenAndDigits(fLists)
# msg = '* Analyzing ({}/{})'
# for i in range(0, xpNum):
#     print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
#     (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
#     name = fLists[i][0].split('/')[-1].split('.')[-2][:-4]
#     # Export plots ------------------------------------------------------------
#     fun.exportTracesPlot(repDta, name, STYLE, PATH_IMG, append='TRA')
#     cl = [i[:-2]+'cc' for i in CLR]
#     monet.exportGeneLegend(sumDta['genotypes'], cl, PATH_IMG+'/plt.png', 500)
# tE = datetime.now()
# print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
# # fun.printExpTerminal(tE-tS, PATH_ROOT, PATH_IMG, PATH_DATA)
# print(monet.PAD)
