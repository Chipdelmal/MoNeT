import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from random import randint

"""
The goal of this script is to find the cummulative ending error for each aggregation level, and generate a violin plot.

For one aggregation level
    For each cluster
        I have the aggregated difference for this cluster, in a time series vector format. 
"""
LAND = 0

if LAND == 0:
    expBaseName = "Yorkeys_AGG_1_"
    pathRoot = "/Users/gillian/Desktop/ClusteringGIllian"
    # sanity check that the truthExperiment is generated with zero error 
    truthExperiment = "/Users/gillian/Desktop/ClusteringGIllian/agg_C002195" 
    expsList = [2, 25, 50, 100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2195] 
else:
    print("LAND is not set. Please set LAND to one of the provided cases.")

def check_run_exists(run, agg_level):
    for cluster_ID in os.listdir(agg_level): 
        cluster_path = os.path.join(agg_level, cluster_ID)
        candidate_path = os.path.join(cluster_path, run)
        if not os.path.exists(candidate_path):
            print("Candidate path", candidate_path, " does not exist.")
            return False
    return True

def write_to_csv(df, name):
    print("Saving ", name)
    print(df)
    np.savetxt(name, df.values, fmt='%d', delimiter=",") # Saves in the order W H E R B

def plot_errors(error_dict):
    fig = plt.figure(figsize=(10,10))
    plt.grid()
    print("Here are the agg levels: ", error_dict.keys())
    candidate_agg_level = None
    for x in error_dict.keys():
        candidate_agg_level = x
    # generate fixed colors 
    colors = [(randint(0, 1), randint(0, 1), randint(0, 1)) for x in range(len(error_dict[candidate_agg_level]))]
    labels = ["W", "H", "E", "R", "B"]

    for agg_level in error_dict.keys():
        agg_num = int(agg_level[1:])
        print("Here is agg_level: ", agg_level)
        for i in range(len(error_dict[agg_level])): 
            plt.scatter(agg_num, error_dict[agg_level][i], c=colors[i], alpha=0.5)
    
    plt.title("Aggregation vs. Cumulative Error")
    plt.xlabel('Aggregation Levels')
    plt.ylabel('Cumulative Error')
    fig.savefig("agg_vs_cumulativeError.jpg")
    patches = [mpatches.Patch(color=color, label=label) for label, color in zip(labels, colors)]
    fig.legend(handles=patches, loc='right')
        # plt.plot(agg_level, error_dict[agg_level])
        # color the indices accordingly 
    plt.show()

def process_node_id(node_id):
	"""
	Prepends node_id with 0's in string format, so that it's 3 digits and can be used as part of the lookup path.
	"""
	node_id = str(node_id)
	# print("Inside process_node: start", node_id)
	while len(node_id) != 6:
		node_id = '0' + node_id
	# print("Inside process_node: end", node_id)
	return node_id

def run_from_beginning():
    all_agg_dict = dict()
    # read in all the aggregation level folders
    for subdir in os.listdir(pathRoot):
        subpath = os.path.join(pathRoot, subdir)
        if os.path.isdir(subpath):
            # read in each cluster in this aggregation level
            cluster_dict = dict()
            all_agg_dict[subpath] = cluster_dict
            print("Created new dictionary for ", subpath)

            # Find a run that exists in every cluster
            candidate_run = None
            for run in os.listdir(os.path.join(subpath, "cluster_0000")):
                b = check_run_exists(run, subpath)
                if b == True:
                    candidate_run = run
                    break
            
            if candidate_run == None:
                print("No common candidate_run was found for aggregation level ", subpath)
            else: 
                # add this run as each cluster key's value pair
                for sub_subdir in os.listdir(subpath): #sub_subdir is cluster_ID
                    sub_subpath = os.path.join(subpath, sub_subdir)
                    cluster_dict[sub_subpath] = os.path.join(sub_subpath, candidate_run)
            
        # Check the dictionary
        print("Checking all_agg_dict")
        for k in all_agg_dict.keys():
            print("Key: ", k)
            print("Has ", len(all_agg_dict[k].keys()), " values in the corresponding dict")
            print("One example of the kvv is ", all_agg_dict[k][all_agg_dict[k].keys()[0]])

    error_dict = dict()
    for agg_level in all_agg_dict.keys():
        cummulative_error_agg_level = None
        cluster_dict = all_agg_dict[agg_level]
        for cluster in cluster_dict.keys():
            df = pd.read_csv(cluster_dict[cluster])
            # take the absolute value of the difference
            df_abs = df.abs()
            df_sum = df.sum(axis=0)
            # if cummulative_error_agg_level == None:
            #     cummulative_error_agg_level = df_sum
            # else:
            try: 
                cummulative_error_agg_level.add(df_sum)
            except:
                cummulative_error_agg_level = df_sum
        print("End of summing all clusters: ")
        # break agg_level on '/'
        name = agg_level.split('/')
        write_to_csv(cummulative_error_agg_level, name[-1] + '_cumulative_cluster_diff.csv')
        
        split_path = agg_level.split('/')
        agg_name = split_path[1][1:]
        print(agg_name)
        agg_name = int(agg_name)
        error_dict[agg_name] = cummulative_error_agg_level

    # At this point, we expect each aggregation level to have a CSV file with its cumulative cluster_diff
    # Note: It will save these CSV files into the same directory as this script. 

def just_run_plots(expsList):
    # Rebuild the dictionary: 
    error_dict = dict()
    for x in expsList: 
        i = process_node_id(x)
        df = np.loadtxt("agg_C"+str(i)+"_cumulative_cluster_diff.csv")
        error_dict["C"+str(i)] = df
    plot_errors(error_dict)


# Problem: 
# 2195 errors should be 0 ..... 

just_run_plots(expsList)