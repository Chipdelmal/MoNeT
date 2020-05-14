#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


USR = 'dsk'
(LAND, DRIVE_ID, SET, STP, AOI, MF) = (
        'tParams', 'LDR', 'island', False, 'HLT', (True, True)
    )
(thresholds, REL_STRT) = ([.05, .10, .25, .50, .75], 1)
drvPars = drv.driveSelector(DRIVE_ID)
(STYLE, DRV, NOI) = (
        aux.STYLE_HLT,
        drvPars.get('HLT'),
        ix.STP if (STP) else ix.PAN
    )
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/{}/'.format(LAND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/Panmictic/{}/{}/'.format(
            LAND, SET
        )
# Setting paths
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
PATH_OUT = PATH_DATA + 'POSTPROCESS/'
monet.makeFolder(PATH_OUT)
# Print terminal info and create folder
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
###############################################################################
# Setting up paths and directories
###############################################################################
gIx = drvPars[AOI]['genotypes'].index('Other')
dtaFldr = PATH_DATA + 'PREPROCESS/'
expFiles = glob.glob(dtaFldr + '*.lzma')
file = expFiles[0]
expData = pkl.load(file, compression="lzma")
