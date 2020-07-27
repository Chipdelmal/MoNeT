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

headers = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group', .05, .10, .25, .50, .75]

filter_values = filter_variables.filter_values
threshold = filter_variables.threshold

def generate_plot(dataframe, threshold, filter_dict, title):
    for key in filter_dict:
        val = filter_dict[key]
        filtered_df = dataframe[dataframe[key] == val]

        x = np.array([(i/100000000) for i in filtered_df['sv']])
        y = np.array([(i/100000000) for i in filtered_df['fitness']])
        z = np.array([(i) for i in filtered_df[threshold]])

        xminmax = [min(x), max(x)]
        yminmax = [min(y), max(y)]

        # np.linspace --> Return evenly spaced numbers over a specified interval.
        #Parameters: start, stop, number of samples to generate
        (xi, yi) = (np.linspace(xminmax[0], xminmax[1], 1000), np.linspace(yminmax[0], yminmax[1], 1000))
        zi = griddata((x,y), z, (xi[None,:], yi[:, None]), method='nearest')
        fig, ax = plt.subplots()
        ax.contour(xi, yi, zi, levels=filter_variables.mapLevels, linewidths=.5, colors='k', alpha=.5)
        htmp = ax.contourf(xi, yi, zi, levels=filter_variables.mapLevels, extend='max', cmap=plt.cm.Purples)
        ax.set(xscale='log', yscale="linear")
        ax.set_xlabel('Standing Variation')
        ax.set_ylabel('Fitness Cost')
        plt.title(filename)
        plt.xlim(1E-6, 1E-2)
        plt.ylim(yminmax[0], yminmax[1])
        cbar = plt.colorbar(htmp)
        plt.show()

#Open up the csv files and concatenate the dataframes
for pathname in glob.glob(directories.path):
    filename = pathname.split("\\")[-1][:-4]
    df = pd.read_csv(pathname)
    df.columns = headers
    generate_plot(df, threshold, filter_values, filename)
