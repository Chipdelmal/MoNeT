import numpy as np
import pandas as pd
import csv
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm

path = r"C:\Users\prisc\Desktop\Marshall Lab\Marshall Lab Data\Contour Plot Data\ultrafine_data\*.csv"
csv_path = r"C:\Users\prisc\Desktop\Marshall Lab\Marshall Lab Data\Contour Plot Data\data\01_HLT_05-WOP.csv"

headers = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group', .05, .10, .25, .50, .75]

threshold = .05
sv = 0
filtered_values = {}


def generate_plot(dataframe, threshold, filter_dict, title):
    for key in filter_dict:
        val = filter_dict[key]
        dataframe = dataframe[dataframe[key] == val]
    xlist = np.log(np.array(dataframe['sv'] / 100000000))
    ylist = np.array(dataframe['fitness']) / 100000000
    zlist = np.array(dataframe[threshold])
    fig1, ax1 = plt.subplots()
    tcf = ax1.tricontourf(xlist, ylist, zlist, cmap=plt.cm.Purples)
    plt.tricontour(xlist,ylist,zlist, colors='k')
    fig1.colorbar(tcf)
    plt.title(title + ' Threshold:' + str(threshold) )
    plt.xlabel('Standing Variation')
    plt.ylabel('Fitness Cost')
    plt.show()

#Open up the csv files and concatenate the dataframes
for pathname in glob.glob(path):
    filename = pathname.split("\\")[-1][:-4]
    df = pd.read_csv(pathname)
    df.columns = headers

    #Need to figure out what we want, dropping Nan & interpolating?
    df = df[df['sv'] > 0].fillna(0).interpolate()
    generate_plot(df, threshold, filtered_values, filename)
