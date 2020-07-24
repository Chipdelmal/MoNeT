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

path = r"C:\Users\prisc\Desktop\Marshall Lab\Marshall Lab Data\Contour Plot Data\ultrafine_data\*.csv"
csv_path = r"C:\Users\prisc\Desktop\Marshall Lab\Marshall Lab Data\Contour Plot Data\ultrafine_data\01_HLT_05-WOP.csv"

headers = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group', .05, .10, .25, .50, .75]
(ngdx, ngdy) = (1000, 1000)
mapLevels = np.arange(0, 4*365, 200)

threshold = .05
sv = 0
resistance = 0

filter_values = filter_variables.filter_values
threshold = filter_variables.threshold

print(filter_values, threshold)


def generate_plot(dataframe, threshold, filter_dict, title):
    for key in filter_dict:
        val = filter_dict[key]
        filtered_df = dataframe[dataframe[key] == val]

        x = filtered_df['sv']
        y = filtered_df['fitness']
        z = filtered_df[threshold]

        x = np.array([(i/100000000) for i in x])
        y = np.array([(i/100000000) for i in y])
        z = np.array([(i) for i in z])

        xminmax = [min(x), max(x)]
        yminmax = [min(y), max(y)]

        # np.linspace --> Return evenly spaced numbers over a specified interval.
        #Parameters: start, stop, number of samples to generate
        (xi, yi) = (np.linspace(xminmax[0], xminmax[1], ngdx), np.linspace(yminmax[0], yminmax[1], ngdy))

        zi = griddata((x,y), z, (xi[None,:], yi[:, None]), method='nearest')

        fig, ax = plt.subplots()
        ax.contour(xi, yi, zi, levels=mapLevels, linewidths=.5, colors='k', alpha=.5)
        htmp = ax.contourf(xi, yi, zi, levels=mapLevels, extend='max', cmap=plt.cm.Purples)

        ax.set(xscale='log', yscale="linear")
        ax.set_xlabel('Standing Variation')
        ax.set_ylabel('Fitness Cost')
        plt.title(filename)
        plt.xlim(1E-6, 1E-2)
        plt.ylim(yminmax[0], yminmax[1])
        cbar = plt.colorbar(htmp)
        plt.show()


#Open up the csv files and concatenate the dataframes
for pathname in glob.glob(csv_path):
    filename = pathname.split("\\")[-1][:-4]
    df = pd.read_csv(pathname)
    df.columns = headers
    generate_plot(df, threshold, filter_values, filename)
