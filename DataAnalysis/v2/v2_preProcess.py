#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import v2_aux as aux
from glob import glob
import v2_gene as gene
import v2_framework as frame
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

###############################################################################
#
###############################################################################
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('dsk', 'LDR', 'HLT')
(OVW, MF, JOB) = (True, (False, True), 1)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, False)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR)
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = aux.getExpPaths(PT_ROT)


frame.preProcessLandscapeV2()
