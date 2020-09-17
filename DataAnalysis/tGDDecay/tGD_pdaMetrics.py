
import numpy as np
import operator as op
import tGD_dataProcess as da
import matplotlib.pyplot as plt

(thi, tho, thw, qnt) = (.35, .75, .5, .9)
# Thresholds ------------------------------------------------------------------
fName = '/media/hdd/WorkExperiments/tGD/figure2/tGD/000/POSTPROCESS/E_000_075_005_090_03_0100-HLT_00_rto.npy'
repsRatios = np.load(fName)
# Thresholds ------------------------------------------------------------------
(reps, days) = repsRatios.shape
(thIBool, thOBool) = (
        da.compRatioToThreshold(repsRatios, thi, op.lt),
        da.compRatioToThreshold(repsRatios, tho, op.gt)
    )
# Time to first introgression -------------------------------------------------
tti = np.argmax(thIBool == 1, axis=1)
tto = np.subtract(days, np.argmin(np.flip(thOBool), axis=1))
# Min and max -----------------------------------------------------------------
(repsMin, repsMax) = (repsRatios.min(axis=1), repsRatios.max(axis=1))
# Window of protection --------------------------------------------------------
thwBool = da.compRatioToThreshold(repsRatios, thw, op.lt)
wop = np.sum(thwBool, axis=1)
# Quantiles -------------------------------------------------------------------
np.nanquantile(tti, qnt)
np.nanquantile(tto, qnt)
np.nanquantile(wop, 1-qnt)

(fig, ax) = plt.subplots(nrows=3, ncols=1)
ax[0].imshow(repsRatios, cmap='Purples_r')
ax[1].imshow(thIBool, cmap='Purples_r')
ax[2].imshow(thOBool, cmap='Purples_r')
# monet.quickSaveFigure(fig, './test.png')
