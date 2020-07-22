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

threshold = .05
sv = 0
filtered_values = {'sv': sv}

# data_dict = {}
# for header in headers:
#     data_dict[header] = []

# all_data = pd.DataFrame.from_dict(data_dict)

def generate_plot(dataframe, threshold, filter_dict, title):
    for key in filter_dict:
        val = filter_dict[key]
        dataframe = dataframe[dataframe[key] == val]
    xlist = np.log(np.array(dataframe['resistance'] ))
    ylist = np.array(dataframe['fitness']) / 100000000
    zlist = np.array(dataframe[threshold])
    fig1, ax1 = plt.subplots()
    tcf = ax1.tricontourf(xlist, ylist, zlist, cmap=plt.cm.Purples)
    plt.tricontour(xlist,ylist,zlist, colors='k')
    fig1.colorbar(tcf)
    plt.title(title + ' Threshold:' + str(threshold) )
    plt.xlabel('Resistance')
    plt.ylabel('Fitness')
    plt.show()

#Open up the csv files and concatenate the dataframes
for pathname in glob.glob(path):
    filename = pathname.split("\\")[-1][:-4]
    df = pd.read_csv(pathname)
    df.columns = headers

    #Need to figure out what we want, dropping Nan & interpolating?
    df = df[df['resistance'] > 0].dropna().interpolate()
    generate_plot(df, threshold, filtered_values, filename)
