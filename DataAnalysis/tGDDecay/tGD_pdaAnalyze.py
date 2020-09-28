import numpy as np
import tGD_aux as aux
from glob import glob
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet

USR = 'chipdelmal'
(thi, tho, QNT) = (.5, .5, '90')
(USR, DRV, exp, AOI) = ('dsk', 'tGD', '000', 'TRS')
# Setup path -----------------------------------------------------------------
# TO DO: Make sure your code now runs with this function. You'll probably have
#           to have a look at tGD_aux.py in line 52 to setup your path correctly.
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_IMG = PT_IMG+'xRay/'
monet.makeFolder(PT_IMG)
# Load file ------------------------------------------------------------------
# TO DO: We need to iterate over this fNames list of files, repeating the plot
#           for each one (this will become a for loop)
fNames = glob(PT_OUT+'*{}*.npy'.format(AOI))
i = 1
fName = fNames[i]
repsRatios = np.load(fName)
f_list = fName.replace('-', '_').split('_')[1:9]
del f_list[6]
f_tuple = tuple(list(map(int, f_list)))
# Load the TTI and TTO from the MLR data files in the SUMMARY folder
# TO DO : Updated these to take the path from above. Check that they are still
#           working correctly.
ttiR = pkl.load(PT_MTR+'{}_TTI_{}_mlr.bz'.format(AOI, QNT))
ttiR.keys()
tti = ttiR[f_tuple][int(thi*100)] # These ID numbers come from the fName
ttoR = pkl.load(PT_MTR+'{}_TTO_{}_mlr.bz'.format(AOI, QNT))
tto = ttoR[f_tuple][int(tho*100)]
# Plotting---------------------------------------------------------------------
(fig, ax) = plt.subplots(nrows=1, ncols=1)
ax.imshow(repsRatios, cmap='Purples_r')
# Style notes: In python you usually don't leave space in-between '=' when
#               its for passing arguments to a function (only for assignment)
# add TTI----------------------------------------------------------------------
[plt.axvline(i, color='#3DFE70', alpha=.75, linewidth=0.2) for i in tti]
# add TTO----------------------------------------------------------------------
[plt.axvline(j, color='#3DFE70', alpha=.75, linewidth=0.2) for j in tto]
# Save the figure--------------------------------------------------------------
outName = fName.split('/')[-1].split('.')[0][:-4]
plt.savefig(PT_IMG+outName+'.png', bbox_inches='tight', pad_inches=0, dpi=500)
# monet.quickSaveFigure(fig, './test.png')
