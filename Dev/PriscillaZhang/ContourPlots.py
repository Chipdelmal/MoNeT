import numpy as np
import pandas as pd
import csv
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm

path = r"C:\Users\prisc\Desktop\Marshall Lab\Marshall Lab Data\Contour Plot Data\data\*.csv"
csv_path = r"C:\Users\prisc\Desktop\Marshall Lab\Marshall Lab Data\Contour Plot Data\data\01_HLT_05-WOP.csv"

headers = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group', .05, .10, .25, .50, .75]
df = pd.read_csv(csv_path, header=None, index_col=None)
df.columns = headers
filtered_df = df[df['resistance'] > 0]
filtered_df


threshold = .25
sv = 10
filtered_values = {'sv': sv}

def generate_plot(dataframe, threshold, filter_dict):
    for key in filter_dict:
        val = filter_dict[key]
        dataframe = dataframe[dataframe[key] == val]

    xlist = np.array(dataframe['resistance']) / 1000000000
    ylist = np.array(dataframe['fitness']) / 100000000
    zlist = np.array(dataframe[threshold])

    fig1, ax1 = plt.subplots()
    tcf = ax1.tricontourf(xlist, ylist, zlist, cmap=plt.cm.Purples)
    plt.tricontour(xlist,ylist,zlist, colors='k')
    fig1.colorbar(tcf)
    plt.show()

generate_plot(filtered_df, threshold, filtered_values)
