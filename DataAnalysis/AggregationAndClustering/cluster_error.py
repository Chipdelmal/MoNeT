import os
import numpy as np
import csv
import MoNeT_MGDrivE as monet

""" 
The goal of this script is to take the difference between an aggregated time series vector, and the full resolution time 
series vector. 
"""

"""
*************************** Input Paths ************************************************************************************* 
"""
path_to_all_experiments = '/RAID5/marshallShare/ERACR/Yorkeys_MINI/Experiemnts'
path_to_aggregated_landscapes = '/RAID5/marshallShare/ERACR/Yorkeys_MINI/LandAggregated'

#path_to_all_experiments = "/Users/gillian/Desktop/GillianDataset/Experiments"
#path_to_aggregated_landscapes = "/Users/gillian/Desktop/GillianDataset/LandAggregated"

gender_mean = "F"
maleToggle, femaleToggle = True, True
ref_dir = "/RAID5/marshallShare/ERACR/Yorkeys_MINI/Experiemnts/C002195"
# end_ref = "/ANALYZED/E_0730_30_20_02_00020/"
population_IDs = ["W", "H", "E", "R", "B"]
# aggregation_levels = ["C000002", "C000025", "C000250", "C001000", "C002195"]
num_runs = 1
output_path = "/RAID5/marshallShare/ERACR/Yorkeys_MINI/OUT/"

# it computes for all provided runs
aggregationDictionary = monet.autoGenerateGenotypesDictionary(
	population_IDs,
	[
		'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
		'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
	]
)

"""
*************************** Functions *************************************************************************************** 
"""
def find_agg_to_listruns(path_to_all_experiments):
	"""
	Given the path to all experiments, builds a dictionary of experiment runs. Lookup by aggregation level. 

	Input: 
		path_to_all_experiments: should be the path of all the experiments
	Output:
		all_run_paths: a list of "aggregation_level/run_id" paths 
		agg_level_dict: a dictionary with key: aggregation_level, value: a list of different experiment runs
	"""
	agg_level_dict = dict()
	all_run_paths = []
	aggregation_levels = [dl for dl in os.listdir(path_to_all_experiments) if os.path.isdir(os.path.join(path_to_all_experiments, dl))]
	for a in aggregation_levels:
		agg_path = os.path.join(path_to_all_experiments, a)
		agg_level_dict[a] = []

		for run in os.listdir(agg_path):
			all_run_paths.append(os.path.join(a, run))
			agg_level_dict[a] += [run]
	return all_run_paths, agg_level_dict


def find_nodes_to_cluster(run_path, path_to_aggregated_landscapes):
	"""
	Reads in the experiment at run_path, and generates a mapping of each node to the cluster ID it's 
	aggregated into. 

	Input:
		run_path: the path specifying which level of aggregation, and which run ID
		path_to_aggregated_landscapes: the path to the LandAggregated folder, holding the cluster summaries

	Output: Returns a dictionary following the below format:
		key: cluster ID
		value: list of node IDs that were aggregated into this cluster
 
	A side effect is a CSV file generated saving a mapping from cluster ID to node ID for a particular 
	aggregation level. For an example, look for a file with "_cluster_summary_".
	"""
	agg_level, run = run_path.split('/')
	agg_level_run = os.path.join(path_to_aggregated_landscapes, run_path)
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
	# agg_level_count = len(np.unique(clusters))
	# assert(agg_level_count == agg_level) # add this in later

	# Save this result into a csv file
	with open(output_path + agg_level + "_cluster_summary_" + run[:len(run) - 2] + ".csv", mode="w") as cluster_summary:
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
	Prepends node_id with 0's in string format, so that it's 3 digits and can be used as part of the lookup path.
	"""
	node_id = str(node_id)
	# print("Inside process_node: start", node_id)
	while len(node_id) != 4:
		node_id = '0' + node_id
	# print("Inside process_node: end", node_id)
	return node_id

def sum_nodes_in_cluster(key, cluster_dict):
	"""
	Gets the summed output vector for the nodes aggregated into each cluster, and calls get_diff_cluster_vs_full to calculate the 
	difference betweeen this aggregation level's summed output vector, and the full resolution output vector. 

	Input:
		key: string that should be used as the key in the dict. Can be parsed for the number of nodes, and the run ID.
		cluster_dict: is a dictionary where cluster ID maps to list of node IDs that cluster summarizes.

	Output: None
		Calls get_diff_cluster_vs_full() writes the summed output difference vector for each of the clusters to the CSV.
	"""
	agg_level, run_id = key.split('/')
	print(agg_level, run_id)

	if not os.path.exists("agg_" + agg_level):
		os.mkdir("agg_" + agg_level)

	clusters = list(cluster_dict.keys())
	# iterate over the clusters
	for c in clusters:
		print("Processing cluster ID ", c)
		nodes_to_summarize = cluster_dict[c]

		if not os.path.exists("agg_" + agg_level + "/cluster_" + process_node_id(c)):
			os.mkdir("agg_" + agg_level + "/cluster_" + process_node_id(c))

		filenames = dict()
		filenames['male'] = []
		filenames['female'] = []

		# grab all the filepaths for one cluster
		for node_id in nodes_to_summarize:
			# print("Here is ", node_id)
			processed_node_id = process_node_id(node_id)

			# pick a run: Yorkeys01_0027_A
			# print(os.listdir(start_ref))
			list_dir = [f for f in os.listdir(ref_dir)]
			i = int(np.random.uniform(0, len(os.listdir(ref_dir))))
			print(i)
			print(len(list_dir))

			# build reference_pop
            		# reference_pop = ref_dir + '/'
			reference_pop = ref_dir + '/' +  end_ref # reference_pop += list_dir[i]
			# reference_pop += end_ref
                        
			file_path = os.path.join(reference_pop + "F_Mean_Patch" + processed_node_id + ".csv")
			filenames['female'].append(file_path)

			file_path = os.path.join(reference_pop + "M_Mean_Patch" + processed_node_id + ".csv")
			filenames['male'].append(file_path)

		# sum all the filepaths inside one cluster, then group by genotypes
		cluster_sum = monet.sumLandscapePopulationsFromFiles(filenames, male=maleToggle, female=femaleToggle, dataType=float)
		# returns a dictionary with 'population' as the time series population vector
		clusterGeno_sum = monet.aggregateGenotypesInNode(cluster_sum, aggregationDictionary)

		# take the difference between the sum and the clustered result
		# male
		male = str(agg_level) + "/" + str(run_id) + "/ANALYZED/E_0730_30_20_02_00020/M_Mean_Patch" + process_node_id(c) + ".csv"
		exp_path_M = os.path.join(path_to_all_experiments, male)
		# female
		female = str(agg_level) + "/" + str(run_id) + "/ANALYZED/E_0730_30_20_02_00020/F_Mean_Patch" + process_node_id(c) + ".csv"
		exp_path_F = os.path.join(path_to_all_experiments, female)

		filenames2 = dict()
		filenames2['male'] = [exp_path_M]
		filenames2['female'] = [exp_path_F]

		agg_sum = monet.sumLandscapePopulationsFromFiles(filenames2, male=maleToggle, female=femaleToggle)
		aggGeno_sum = monet.aggregateGenotypesInNode(agg_sum, aggregationDictionary)

		# take the difference between the aggregated_sum vector and the full unaggregated sum vector, writes it to CSV
		get_diff_cluster_vs_full(aggGeno_sum, clusterGeno_sum, "agg_" + agg_level + "/cluster_" + process_node_id(c) + "/run_" + run_id + str(maleToggle) + str(femaleToggle))


def get_diff_cluster_vs_full(aggGeno_sum, clusterGeno_sum, name):
	"""
	Takes path to cluster_id run in Experiments/,
	as well as the cluster_sum, which is the sum of all the nodes in that cluster_id.

	Input: 
		aggGeno_sum: dict representing the full resolution of nodes.
		clusterGeno_sum: dict representing the aggregated clusters.
		name: rseulting difference vector csv's name.

	Output: None

	"""
	# print("AGG_GENO_RESULT: ", aggGeno_sum['population'].shape)
	# print("CLUSTER_GENO_RESULT: ", clusterGeno_sum['population'].shape)

	result = np.subtract(aggGeno_sum['population'], clusterGeno_sum['population']); print(name); os.makedirs(os.path.dirname(output_path), exist_ok=True);
        with open(output_path + name + ".csv", mode="w") as cluster_summary:
		result_writer = csv.writer(cluster_summary)
		result_writer.writerow(population_IDs) # labels
		for r in result:
			result_writer.writerow(r)

def compare_all_aggregations_once(agg_level_dict):
	"""
	Iterates over each aggregation level and samples randomly for an experiment run. 

	Input: 
		agg_level_dict: dictionary of agg_level to list of experimnt runs' paths. 

	Output: None
		A side effect of find_nodes_to_cluster() saves a CSV of each node mapped to the cluster ID in a particular aggregation level. 
		A side effect of sum_nodes_in_cluster()->get_diff_cluster_vs_full saves the difference vector into a CSV.
	"""
	# iterate over all of the aggregation levels
	print("Available aggregation_levels to use as keys to agg_level_dict: ", agg_level_dict.keys())
	for key in agg_level_dict.keys():
		# sample randomly over runs provided
		i = int(np.round(np.random.uniform(0, len(agg_level_dict[key]) - 1)))
		# generate the run_path 
		run_path = key + "/" + agg_level_dict[key][i]
		print("Running for key: ", key, " and run: ", agg_level_dict[key][i])
		# generate a dict of clusterIDs to nodeIDs aggregated into that cluster
		aggData = find_nodes_to_cluster(run_path, path_to_aggregated_landscapes)
		# sums an output difference vector for each cluster
		sum_nodes_in_cluster(run_path, aggData)


## MAIN

## STEP 1: Create mapping from aggregated to not aggregated in csv
all_run_paths, agg_level_dict = find_agg_to_listruns(path_to_all_experiments)

# STEP 2: Sum all nodes in a cluster and generate difference
# for i in range(num_runs):
	# call compare_all_aggregations_once to iterate over each aggregation level and sample randomly
#	compare_all_aggregations_once(agg_level_dict)

# run_dict = dict()
# for run_path in all_run_paths:
# 	run_dict[run_path] = find_nodes_to_cluster(run_path, path_to_aggregated_landscapes)
# 	cluster_run_sum = sum_nodes_in_cluster(run_path, run_dict[run_path])

# Previously used for testing, hardcoded
# key = 'C000250/Yorkeys01_0000_A' # 250 nodes, run 0
# run = run_dict[key] # dictionary for that run
# cluster_run_sum = sum_nodes_in_cluster(key, run)

# STEP 2: Sum all nodes in a cluster and generate difference
# Find all the dirs in the ref_dir
ref_dir_runs = os.listdir(ref_dir)
for i in range(num_runs): 
    ref_sample = int(np.round(np.random.uniform(0, len(ref_dir_runs) - 1)))
    end_ref = ref_dir_runs[ref_sample] + "/ANALYZED/E_0730_30_20_02_00020/"
    print("ref_dir: ", ref_dir)
    print("end_ref: ", end_ref)
    compare_all_aggregations_once(agg_level_dict)
