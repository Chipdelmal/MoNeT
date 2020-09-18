#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import v2_aux as aux
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

###############################################################################
#
###############################################################################
(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(FMT, OVW, MF, JOB) = ('bz2', True, (False, True), 1)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, False)
EXP = ('000', ) #, '001', '005', '010', '100')
