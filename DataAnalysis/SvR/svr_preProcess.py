#!/usr/bin/python
# -*- coding: utf-8 -*-

import svr_aux as aux
import svr_gene as drv
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = ('dsk', 'LDS', 'HLT')
# Auto settings ---------------------------------------------------------------
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, False)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
drive = drv.driveSelector(DRV)
