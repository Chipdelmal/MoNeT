#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import odeint

pathRoot = "/Volumes/marshallShare/Clovis/"

latLongs = pd.read_csv(pathRoot + "Clovis_coords.csv")
llPlot = latLongs.plot.scatter(x='long', y='lat', c='DarkBlue', alpha=.5)
llPlot.set_xlim(min(latLongs["long"]), max(latLongs["long"]))
llPlot.set_ylim(min(latLongs["lat"]), max(latLongs["lat"]))





# Change these values based on graphical fit
Kp = 1
taus = 31
zeta = .21

# Transfer Function
#  Kp / (taus * s**2 + 2 * zeta * taus * s + 1)
num = [Kp]
den = [taus**2,2.0*zeta*taus,1]
sys1 = signal.TransferFunction(num,den)
t1,y1 = signal.step(sys1)

plt.figure(1)
plt.plot(t1,y1,'b--',linewidth=3,label='Transfer Fcn')
plt.xlabel('Time')
plt.ylabel('Response (y)')
plt.legend(loc='best')
plt.show()
