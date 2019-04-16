import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
import plotly.plotly as py
import numpy as np
import pandas as pd
from __future__ import division
from sklearn.linear_model import LinearRegression
import time

###############################################################################
# MCR Construct
###############################################################################
#------------------------------------------------------------------------------
# Analyzing different metrics on drive behavior
#------------------------------------------------------------------------------
#experiments = ['eta1e-05', 'eta5e-04', 'eta1e-04', 'eta5e-03',
#'eta1e-03', 'eta5e-03', 'eta1e-02', 'eta5e-01', 'eta1e-01',
# 'eta1','eta10', 'eta100','eta1000', 'eta10000','eta1e+05']

#eriments =  ['eta1e-05', 'eta1e-04', 'eta1e-03', 'eta1e-02',  'eta1e-01', 'eta1', 'eta100','eta1000', 'eta10000','eta1e+05']
iteration = 3
pathRoot = "/Users/Biyonka/Desktop/Output/1clustering_analysis/drive_output/"
#gets list of all folders
path = monet.listDirectoriesWithPathWithinAPath(pathRoot)
#get filenames witout the iter
etas = []
for  index,experiment in enumerate(path):
    no_iter = experiment.split("_")[:-1]
    #get filenames without the iter
    ex = "_".join(no_iter)
    if ex not in etas:
        etas.append(ex)

num_exp = len(path)
num_eta = int(num_exp/iteration)
thres, rate, prop_exceeds = [None]*num_exp, [None]*num_exp, [None]*num_eta
eta_analyzed = 0

for index, ex in enumerate(etas):
    count_exceeds = 0
    #get eta value
    eta_iter = ex.split("/")[-1]
    e = eta_iter.split("_")[0][3:]

    for i in range(1, iteration+1, 1):
        path = ex +"_iter" +str(i)+  "/ANALYZED/"
        # Define the experiment's path, aggregation dictionary, and read filenames
        experimentString = "0001"#'{0:04d}'.format(i)
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "H", "R", "B"],
            [
                [0, 0, 1, 2, 3],
                [1, 4, 4, 5, 6],
                [2, 5, 7, 7, 8],
                [3, 6, 8, 9, 9]
            ]
        )
        filenames = monet.readExperimentFilenames(path + experimentString)
        # To analyze a single node ...................................................
        # Load a single node (auxiliary function just for demonstration)
        nodeIndex = 0
        nodeData = monet.loadNodeData(
            filenames.get("male")[nodeIndex], filenames.get("female")[nodeIndex],
            dataType=float
        )

        # To analyze the sum of the whole landscape ..................................
        # Sum landscape into one array ("in place" memory-wise)
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )

        # Aggregate genotypes (node or landscape) ....................................
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData,
            aggregationDictionary
        )

        #get first time that exceeds threshold
        m = max(aggData['population'][:, 1])
        threshold = 0.9*m
        t1 = filter(lambda x: x[1]>30, enumerate(aggData['population'][:, 1]))[0][0]
        #get first time that is greater than 4000
        t2 = filter(lambda x: x[1]<threshold, enumerate(aggData['population'][:, 1]))[-1][0]
        rate_est = (threshold-30)/(t2-t1)
        rate[i-1+iteration*index] = (e, rate_est)#append((e, rate_est))

        #Get time exceeds proportion 0.9
        allele_avg = np.mean(np.sum(aggData['population'], axis =1))
        homing = aggData['population'][:, 1]
        #get time at which homing ratio exceeds threshold
        if any(homing >= 0.90*allele_avg):
            #get first time that ratio exceeds 0.9
            time = (list(homing>= 0.90*allele_avg)).index(True)
            #keep count of number of times this occurs
            count_exceeds += 1
        else:
            # if threshold of homing never exceeds 0.9, set time to be 0
            time = 0#aggData['population'].shape[0]
        thres[i-1+iteration*index] =(e, time)

    prop_exceeds[eta_analyzed] = (e, count_exceeds/iteration)
    eta_analyzed += 1
    #after each set of iterations, write csv of rate and threshold results
    intermediate_thres = [x for x in thres if x is not None]
    intermediate_rate = [x for x in rate if x is not None]
    eta, metric_thres = zip(*intermediate_thres)
    eta2, metric_rate = zip(*intermediate_rate)
    df = pd.DataFrame({"eta":  eta, "thres": metric_thres, 'rate': metric_rate})
    df.to_csv("thresrate_data_eta"+ str(e) + ".csv", index = False)

# eta, threshold = zip(*thres)
# eta2, metric_rate = zip(*rate)
# df_prev = pd.DataFrame({"eta":  eta, "thres": metric_thres, 'rate': metric_rate})

eta3, metric_prop = zip(*prop_exceeds)
df_prop = pd.DataFrame({"eta":  eta3, 'prop': metric_prop})
df_prop.to_csv("proportion_data.csv", index = False)
