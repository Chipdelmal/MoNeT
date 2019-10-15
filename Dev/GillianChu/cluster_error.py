import os
import numpy as np
import csv

experiments_path = "/Users/gillian/Desktop/GillianDataset/Experiments"
land_aggregated_path = "/Users/gillian/Desktop/GillianDataset/LandAggregated"
gender_mean = "F"

# STEP 1 FUNCTIONS 

# Finds the paths to each aggregation level
def getExperimentPaths(experiments_path):
	"""
	Gives a list of aggregation_level/run_id folder names saved at the provided experiments_path.
	"""
	run_paths = []
	aggregation_levels = [dl for dl in os.listdir(experiments_path) if os.path.isdir(os.path.join(experiments_path, dl))]
	for a in aggregation_levels:
		agg_path = os.path.join(experiments_path, a)
		for run in os.listdir(agg_path):
			run_paths.append(os.path.join(a, run))
	return run_paths

def getAggregation(run_path, land_aggregated_path):
	"""
	run_path: the path specifying which level of aggregation, and which run ID
	land_aggregated_path: the path to the LandAggregated folder, holding the cluster summaries

	Returns a dictionary following the below format:
	key: cluster ID
	value: list of node IDs that were aggregated into this cluster

	This is also saved into a csv file as a result of running this function.
	"""
	agg_level, run = run_path.split('/')
	agg_level_run = os.path.join(land_aggregated_path, run_path)
	agg_level_edited = agg_level_run[:len(agg_level_run) - 1]
	agg_level_edited += "I.csv"

	reader = csv.reader(open(agg_level_edited, "r"))
	x = np.array(list(reader))
	# print(x[0]) # Confirm here are the headers

	ids = np.array(x[1:,0]).astype(int)
	clusters = np.array(x[1:,3]).astype(int)
	result = list(zip(clusters, ids))
	result.sort(key=lambda x: x[0])

	# Count num clusters
	agg_level_count = len(np.unique(clusters))
	# assert(agg_level_count == agg_level) # add this in later

	# Save this result into a csv file
	with open(agg_level + "_cluster_summary_" + run[:len(run) - 2] + ".csv", mode="w") as cluster_summary:
		result_writer = csv.writer(cluster_summary)
		result_writer.writerow(["Cluster ID", "Node ID"]) # labels
		for r in result:
			result_writer.writerow(r)
	
	# put into dict with:
	# key: cluster ID, value: 
	result_dict = dict()
	for c, i in result:
		if c not in result_dict.keys():
			result_dict[c] = [i]
		else:
			result_dict[c].append(i)

	# return dictionary
	return result_dict 

# STEP 2 FUNCTIONS
def process_node_id(node_id):
	"""
	Prepends node_id with 0's in string format
	"""
	node_id = str(node_id)
	while len(node_id) != 4:
		node_id = '0' + node_id
	return node_id

def getSum(key, run):
	"""
	key tells the number of nodes, and the run ID
	run is a dictionary where cluster ID maps to list of node IDs that cluster summarizes

	Output:
	the summed output vector for each of the clusters
	"""
	agg_level, run_id = run_path.split('/')

	clusters = list(run.keys())
	for c in clusters:
		# print("Processing cluster ID ", c)
		nodes_to_summarize = run[c]
		# cluster_sum = 

		for node_id in nodes_to_summarize:
			# print("Here is ", node_id)
			pni = process_node_id(node_id)
			getMatrix(pni, agg_level, run_id)
		# for each node, retrieve its matrix

def getMatrix(node_id, agg_level, run_id):
	agg_path = os.path.join(experiments_path, agg_level)
	run_path = os.path.join(agg_path, run_id + "/ANALYZED")
	for dl in os.listdir(run_path):
		run_spec_path = os.path.join(run_path, dl)
		file_path = os.path.join(run_spec_path, "F_Mean_Patch" + node_id + ".csv")

		# get matrix from this file_path

		## START HERE 


## MAIN 

## STEP 1: Create mapping from aggregated to not aggregated in csv

run_paths = getExperimentPaths(experiments_path)

run_dict = dict()
for run_path in run_paths:
	run_dict[run_path] = getAggregation(run_path, land_aggregated_path)

# for k in run_dict.keys():
# 	print(k) #, run_dict[k])

# STEP 2: Sum all nodes in a cluster

# pick one run of a cluster, HARD CODED FOR NOW, 
# TODO: Sample the run randomly

key = 'C000250/Yorkeys01_0000_A' # 250 nodes, run 0
run = run_dict[key] # dictionary for that run

cluster_run_sum = getSum(key, run)



# Extension:
# Do this error calculation for some segment of the total nodes (i.e. for one cluster) ? 
