
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import STP_functions as fun
import STP_plots as plo


plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
})


PTH_pts = '/media/hdd/WorkExperiments/STP/'
pts = pd.read_csv(PTH_pts+'stp_all_sites_v5.csv')
(BLAT, BLNG) = ((-0.045, .5), (6.4, 6.8))
# #############################################################################
# Map
# #############################################################################
(fig, ax) = plt.subplots(figsize=(10, 10))
(fig, ax) = plo.plotMap(fig, ax, pts, BLAT, BLNG)