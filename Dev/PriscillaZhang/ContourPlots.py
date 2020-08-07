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
import ContourPlots_FilterVariables as filter_variables
import ContourPlots_directories as directories
from joblib import Parallel, delayed
from math import sqrt

headers = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group', .05, .10, .25, .50, .75]

filter_values = filter_variables.filter_values
threshold = filter_variables.threshold

def generate_plot(dataframe, threshold, filter_dict, title):
    for key in filter_dict:
        val = filter_dict[key]
        filtered_df = dataframe[dataframe[key] == val]

        x = np.array([(i/100000000) for i in filtered_df['sv']])
        y = np.array([(i/100000000) for i in filtered_df['fitness']])
        z = np.array(filtered_df[threshold])

        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)

        # np.linspace --> Return evenly spaced numbers over a specified interval.
        #Parameters: start, stop, number of samples to generate
        (xi, yi) = (np.linspace(xmin, xmax, 500), np.linspace(ymin, ymax, 500))
        zi = griddata((x,y), z, (xi[None,:], yi[:, None]), method='nearest')
        fig, ax = plt.subplots()
        ax.contour(xi, yi, zi, levels=filter_variables.mapLevels, linewidths=.5, colors='k')
        heatmap = ax.contourf(xi, yi, zi, levels=filter_variables.mapLevels, extend='max', cmap=plt.cm.Purples)
        ax.set(xscale='log')
        ax.set_xlabel('Standing Variation')
        ax.set_ylabel('Fitness Cost')
        plt.title(title.split("\\")[-1][:-4])
        plt.xlim(1E-6, 1E-2)
        plt.ylim(ymin, ymax)
        cbar = plt.colorbar(heatmap)
        plt.show()


#Open up the csv files and concatenate the dataframes
# for pathname in glob.glob(directories.path):
#     filename = pathname.split("\\")[-1][:-4]
#     df = pd.read_csv(pathname)
#     df.columns = headers
#     generate_plot(df, threshold, filter_values, filename)

def read_generate(pathname):
    df = pd.read_csv(pathname)
    df.columns = headers
    filename = pathname
    generate_plot(df, threshold, filter_values, filename)

Parallel(n_jobs=2)(delayed(read_generate)(pathname) for pathname in glob.glob(directories.path))
