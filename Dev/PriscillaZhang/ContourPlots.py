import numpy as np
import pandas as pd
import csv
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from scipy.interpolate import griddata
import sys
import ContourPlots_Variables as variables
import ContourPlots_directories as directories
import ContourPlots_functions as functions
from joblib import Parallel, delayed


Parallel(n_jobs=4)(delayed(functions.read_generate)(pathname) for pathname in glob.glob(directories.path))
