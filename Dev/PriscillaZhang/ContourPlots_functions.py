import numpy as np
import pandas as pd
import ContourPlots_Variables as variables
import ContourPlots as contourplot

def read_generate(pathname):
    df = pd.read_csv(pathname)
    df.columns = variables.headers
    filename = pathname.split("\\")[-1][:-4]
    contourplot.generate_plot(df, threshold, filter_values, filename)
