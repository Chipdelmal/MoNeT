import numpy as np
import operator as op
import tGD_dataProcess as da
import matplotlib.pyplot as plt
import compress_pickle as pkl

USR = 'ameek'
(thi, tho, thw, QNT) = (.35, .75, .5, '90')
# Setup path -----------------------------------------------------------------
if USR == 'chipdelmal':
    pth = '/media/hdd/WorkExperiments/tGD/figure2/tGD/000/POSTPROCESS/'
elif USR == 'ameek':
    pth = '/Volumes/GoogleDrive/.shortcut-targets-by-id/1e56Nrp5mAxkyQ0C2zgBXCJ1YMFa2QNXg/AmeekBindra/tGD/000/POSTPROCESS/'
# Load file ------------------------------------------------------------------
fName = 'E_005_075_005_090_02_0100-HLT_00_rto.npy'
repsRatios = np.load(pth+fName)
# Thresholds -----------------------------------------------------------------
# (reps, days) = repsRatios.shape
# (thIBool, thOBool) = (
#         da.compRatioToThreshold(repsRatios, thi, op.lt),
#         da.compRatioToThreshold(repsRatios, tho, op.gt)
#     )
# # Time to first introgression ------------------------------------------------
# tti = np.argmax(thIBool == 1, axis=1)
# tto = np.subtract(days, np.argmin(np.flip(thOBool), axis=1))
# # Min and max ----------------------------------------------------------------
# (repsMin, repsMax) = (repsRatios.min(axis=1), repsRatios.max(axis=1))
# # Window of protection -------------------------------------------------------
# thwBool = da.compRatioToThreshold(repsRatios, thw, op.lt)
# wop = np.sum(thwBool, axis=1)
# # Quantiles ------------------------------------------------------------------
# (ttiQ, ttoQ, wopQ) = (
#         np.nanquantile(tti, qnt),
#         np.nanquantile(tto, qnt),
#         np.nanquantile(wop, 1-qnt)
#     )

# fName
f_list = fName.replace('-', '_').split('_')[1:9]
del f_list[6]
f_tuple = tuple(list(map(int, f_list)))

# Load the TTI and TTO from the MLR data files in the SUMMARY folder
ttiR = pkl.load('/Volumes/GoogleDrive/.shortcut-targets-by-id/1e56Nrp5mAxkyQ0C2zgBXCJ1YMFa2QNXg/AmeekBindra/tGD/000/SUMMARY/HLT_TTI_{}_mlr.bz'.format(QNT))
ttiR.keys()
tti = ttiR[f_tuple][int(QNT)] # These ID numbers come from the fName

ttoR = pkl.load('/Volumes/GoogleDrive/.shortcut-targets-by-id/1e56Nrp5mAxkyQ0C2zgBXCJ1YMFa2QNXg/AmeekBindra/tGD/000/SUMMARY/HLT_TTO_{}_mlr.bz'.format(QNT))
ttoR.keys()
tto = ttoR[f_tuple][int(QNT)]
# ameek's scratch
#print(ttiR.keys())
#ttiR[] = {ttiR}
#tti = ttiR[(5, 75, 5, 90, 2, 100, 0)][int(QNT)]
#tto =

# Plotting---------------------------------------------------------------------
(fig, ax) = plt.subplots(nrows=1, ncols=1)
ax.imshow(repsRatios, cmap='Purples_r')
# add TTI----------------------------------------------------------------------
[plt.axvline(i, color = 'pink', alpha = 75, linewidth = 0.5) for i in tti]
# add TTO----------------------------------------------------------------------
[plt.axvline(j, alpha = 75, linewidth = 0.5) for j in tto]
# Save the figure--------------------------------------------------------------
plt.savefig("test_heatmap.png", bbox_inches = 'tight', pad_inches = 0)
# monet.quickSaveFigure(fig, './test.png')
