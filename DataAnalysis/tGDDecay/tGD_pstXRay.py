#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_gene as drv
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(gIx, hIx) = (1, 0)

EXP = ('000', )  # '001', '005', '010', '100')

# This will become a for-loop
exp = EXP[0]
# Selects the working directories
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
outputFolder = PT_IMG + 'xray/'
monet.makeFolder(outputFolder)
# Gets the paths of the numpy arrays
filepaths = sorted(glob(PT_OUT+'E_*'))
outputFolder

# Load the numpy array (should become a for-loop)
fPath = filepaths[10]
repsRatios = np.load(fPath)
# Setup the plot (should use the hIx color)
(fig, ax) = plt.subplots(nrows=1, ncols=1)
ax.imshow(repsRatios, cmap='Purples_r')



#################### COLOR THING ###########################################
drive = drv.driveSelector(DRV, AOI)
drive['colors']
