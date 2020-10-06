import numpy as np
import tGD_aux as aux
from glob import glob
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
import re

USR = 'ameek'

(thi, tho, QNT) = (.5, .5, '90')
(USR, DRV, exp, AOI) = ('ameek', 'tGD', '000', 'TRS')

# Select path ------------------------------------------------------------------

(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_IMG = PT_IMG+'xRay/'
monet.makeFolder(PT_IMG)


# Load file ------------------------------------------------------------------
fNames = glob(PT_OUT+'*.npy'.format(AOI))

for fName in fNames:

    # Name formatting -> tuple---------------------------------------------------------------------
    repsRatios = np.load(fName)
    fList = re.split(r'[a-zA-Z_/.-]+', fName)[9:16]
    fKeys = tuple(list(map(int, fList)))
    AOI = re.split(r'[0-9_./-]+', fName)[18]

    # Select cmap ------------------------------------------------------------------
    (scalers, HD_DEP, IND_RAN, palette) = aux.selectDepVars('TTI', AOI)
    cmap_reversed = palette.reversed()


    # load TTI and TTO ------------------------------------------------------------------
    ttiR = pkl.load(PT_MTR+'{}_TTI_{}_mlr.bz'.format(AOI, QNT))
    tti = ttiR[fKeys][int(thi*100)]
    ttoR = pkl.load(PT_MTR+'{}_TTO_{}_mlr.bz'.format(AOI, QNT))
    tto = ttoR[fKeys][int(tho*100)]

    # Plotting---------------------------------------------------------------------
    (fig, ax) = plt.subplots(nrows=1, ncols=1)
    ax.imshow(repsRatios, cmap=cmap_reversed)

    # add TTI----------------------------------------------------------------------
    [plt.axvline(i, color='#3DFE70', alpha=.75, linewidth=0.2) for i in tti]
    # add TTO----------------------------------------------------------------------
    [plt.axvline(j, color='#3DFE70', alpha=.75, linewidth=0.2) for j in tto]
    # Save the figure--------------------------------------------------------------
    outName = fName.split('/')[-1].split('.')[0][:-4]
    plt.savefig(PT_IMG+outName+ '.png', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close("all")
