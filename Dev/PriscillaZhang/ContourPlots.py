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


data_dict = {}
for header in headers:
    data_dict[header] = []

all_data = pd.DataFrame.from_dict(data_dict)

#Open up the csv files and concatenate the dataframes
for filename in glob.glob(path):
    df = pd.read_csv(filename)
    df.columns = headers
    all_data = pd.concat([df, all_data])


filtered_df = all_data[all_data['resistance'] > 0].dropna()
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
