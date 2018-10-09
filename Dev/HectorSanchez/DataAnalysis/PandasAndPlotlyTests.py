import csv
import pandas as pd
import numpy as np
import os
import sys
import matplotlib
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
offline.init_notebook_mode()

offline.iplot([{"y": [1, 2, 1]}])

# Define paths for experiment
pathBase="/Users/sanchez.hmsc/odrive/MGDrivE_Experiments/"
pathExperiment="MCR/ProcessedData/MCRProcessedDataset/"

# Define file name
filename="E_065processedData.csv"

# Load file's contents
pathBase
df=pd.read_csv(pathBase+pathExperiment+filename)

# Day to filter
day=999
columnNames=df.columns.values
columnNames


subset=df[(df['Day'] == day) & (df['HFitness'] >= .1)]
subset


data = [
    go.Heatmap(
        z='H',
        x='FemaleDeposition',
        y='BFitness',
        colorscale='Viridis',
    )
]
fig = go.Figure(data=data, layout=layout)
offline.iplot(fig, filename='datetime-heatmap')






# Define paths for experiment
pathBase="/Users/sanchez.hmsc/odrive/MGDrivE_Experiments/"
pathExperiment="MCR/MCRFitted/E_03_02_0001_0010/0001/"
filename="ADM_Run001_Patch0000.csv"

df=pd.read_csv(pathBase+pathExperiment+filename)
columnNames=df.columns.values
columnNames

# Create a trace
trace = go.Scatter(
    x = df['Time'],
    y = df['HH']
)
data = [trace]
offline.iplot(data, filename='basic-line')

df
