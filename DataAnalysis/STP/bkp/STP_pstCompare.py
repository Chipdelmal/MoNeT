#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import STP_aux as aux
import STP_fun as fun
from glob import glob


(SIG, PRB) = ('island', 'islandnonGravid')
(LVL, SVA, GRP) = ('090', '1000', '000')
###############################################################################
(USR, XPM, LAND) = ('dsk', 'wfu', 'gravidReleases')
(DRV, STP, SKP, FMT) = ('LDR', True, False, '.lzma')
(THR, QNT) = ([.05, .50], .95)
ptrnMtch = '{}RES-{}-{}-{}.csv*'
###############################################################################
# Reading Dataframes
###############################################################################
# Signal
(PBAS, PIMG, POUT, PPRE, PPST) = aux.selectPath(USR, LAND, SIG, DRV)
sig = fun.readResDF(PPST, LVL, SVA, GRP, ptrnMtch=ptrnMtch)
# Probe
(PBAS, PIMG, POUT, PPRE, PPST) = aux.selectPath(USR, LAND, PRB, DRV)
prb = fun.readResDF(PPST, LVL, SVA, GRP, ptrnMtch=ptrnMtch)
###############################################################################
diff = sig.subtract(prb)
diff


POUT
