
import sys
import numpy as np
import tGD_aux as aux
from glob import glob
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from datetime import datetime
import pandas as pandas
from joblib import Parallel, delayed


(thi, tho, QNT) = (.1, .1, '90')
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('ameek', 'tGD', 'HLT')
X_RAN = [0, 5*365/3]
EXPS = ('000', )

def parallelPlotter(i, xpNum, digs, fName, PT_IMG):
    xpNumCS = str(i + 1).zfill(4)
    print('* Exporting {}/{}'.format(xpNumCS, xpNumS), end='\r')
    # Name formatting -> tuple--------------------------------------------
    repsRatios = np.load(fName)
    fList = fName.split('/')[-1].split('-')[0].split('_')[1:]
    fList.append(fName.split('/')[-1].split('-')[1].split('_')[1])
    fKeys = tuple(list(map(int, fList)))
    # Select cmap --------------------------------------------------------
    (scalers, HD_DEP, IND_RAN, palette) = aux.selectDepVars('TTI', AOI)
    cmap = palette.reversed()
    # load TTI and TTO ---------------------------------------------------
    ttiR = pkl.load(PT_MTR+'{}_TTI_{}_mlr.bz'.format(AOI, QNT))
    tti = ttiR[fKeys][int(thi*100)]
    ttoR = pkl.load(PT_MTR+'{}_TTO_{}_mlr.bz'.format(AOI, QNT))
    tto = ttoR[fKeys][int(tho*100)]
    # Plotting-------------------------------------------------------------
    (fig, ax) = plt.subplots(nrows=1, ncols=1)
    ax.imshow(repsRatios, cmap=cmap)
    # add TTI-------------------------------------------------------------
    [plt.axvline(i, color='black', alpha=.65, lw=0.175, ls='-.') for i in tti]
    # add TTO-------------------------------------------------------------
    [plt.axvline(j, color='black', alpha=.75, lw=0.2, ls='dotted') for j in tto]
    # Save the figure------------------------------------------------------
    outName = fName.split('/')[-1].split('.')[0][:-4]
    plt.xlim(X_RAN)
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)
    plt.savefig(PT_IMG+outName + '.png', bbox_inches='tight', pad_inches=0.01, dpi=500)
    plt.close("all")

for exp in EXPS:
    # Select path ------------------------------------------------------------
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
    PT_IMG = PT_IMG+'xRay/'
    monet.makeFolder(PT_IMG)
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_MTR, tS, 'X-Ray '+AOI)
    # Load file --------------------------------------------------------------
    fNames = glob(PT_OUT+'*{}*.npy'.format(AOI))
    xpNumS = str(len(fNames)).zfill(4)
    (xpNum, digs) = monet.lenAndDigits(fNames)

    Parallel(n_jobs=1)(delayed(parallelPlotter)(i, xpNum, digs, fName, PT_IMG) for (i, fName) in enumerate(fNames))
