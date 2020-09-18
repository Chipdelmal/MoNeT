#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_gene as drv
import tGD_plots as plot


# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('dsk', 'linkedDrive', 'HLT')
(SKP, QNT, OVW) = (False, .90, True)
(gIx, hIx) = (1, 0)
