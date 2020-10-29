

import numpy as np
from glob import glob
import SDY_aux as aux
import SDY_gene as drv
import SDY_land as lnd
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, AOI, THS, QNT) = ('dsk', 'WLD', 0.5, '50')
(DRV, EXP, KEY) = ('SD', 'factorial', '1_005_010_02_020')
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
drive = drv.driveSelector(DRV, AOI)
(DVP, NOI) = (drive.get('gDict'), (lnd.ixYK, lnd.ixTP))
colors = drive['colors']
nodes = lnd.IX
# #############################################################################
# Load mean response
# #############################################################################
popFiles = glob(PT_PRE + '*' + KEY + '*' + AOI + '*sum*')
repRto = [pkl.load(i) for i in popFiles]
repRto
