import os
import numpy as np
import csv
import MoNeT_MGDrivE as monet

experiments_path = '/Volumes/marshallShare/ERACR/Yorkeys_MINI/Experiemnts'
land_aggregated_path = '/Volumes/marshallShare/ERACR/Yorkeys_MINI/LandAggregated'
#experiments_path = "/Users/gillian/Desktop/GillianDataset/Experiments"
#land_aggregated_path = "/Users/gillian/Desktop/GillianDataset/LandAggregated"
gender_mean = "F"
maleToggle, femaleToggle = True, True

"""
Note: reference_pop below is hardcoded because it's the folder where we expect to find all of the nodeIDs available
"""
start_ref = "/Users/gillian/Desktop/GillianDataset/Experiments/C002195/"
finish_ref = "/ANALYZED/E_0730_30_20_02_00020/"
population_IDs = ["W", "H", "E", "R", "B"]
aggregation_levels = ["C000002", "C000025", "C000250", "C001000", "C002195"]
num_runs = 1
# it computes for rall provided runs
aggregationDictionary = monet.autoGenerateGenotypesDictionary(
    population_IDs,
    [
        'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
        'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
    ]
)
# STEP 1 FUNCTIONS

# Finds the paths to each aggregation level
def getExperimentPaths(experiments_path):
	"""
	Gives a list of aggregation_level/run_id folder names saved at the provided experiments_path.
	"""
	counts = dict()
	run_paths = []
	aggregation_levels = [dl for dl in os.listdir(experiments_path) if os.path.isdir(os.path.join(experiments_path, dl))]
	for a in aggregation_levels:
		agg_path = os.path.join(experiments_path, a)
		counts[a] = []

		for run in os.listdir(agg_path):
			run_paths.append(os.path.join(a, run))
			counts[a] += [run]
	return run_paths, counts


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
	# print("Inside process_node: start", node_id)
	while len(node_id) != 4:
		node_id = '0' + node_id
	# print("Inside process_node: end", node_id)
	return node_id

def getSum(key, run):
	"""
	key tells the number of nodes, and the run ID
	run is a dictionary where cluster ID maps to list of node IDs that cluster summarizes

	Output:
	the summed output vector for each of the clusters
	"""
	agg_level, run_id = key.split('/')
	print(agg_level, run_id)

	if not os.path.exists("agg_" + agg_level):
		os.mkdir("agg_" + agg_level)

	clusters = list(run.keys())
	for c in clusters:
		print("Processing cluster ID ", c)
		nodes_to_summarize = run[c]

		if not os.path.exists("agg_" + agg_level + "/cluster_" + process_node_id(c)):
			os.mkdir("agg_" + agg_level + "/cluster_" + process_node_id(c))

		filenames = dict()
		filenames['male'] = []
		filenames['female'] = []

		# grab all the filepaths for one cluster
		for node_id in nodes_to_summarize:
			# print("Here is ", node_id)
			processed_node_id = process_node_id(node_id)

			#pick a run: Yorkeys01_0027_A
			list_dir = [f for f in os.listdir(start_ref) if os.path.isfile(f)]
			i = int(np.round(np.random.uniform(0, len(os.listdir(start_ref)) )))

			#build reference_pop
			reference_pop = list_dir[i]
			reference_pop += finish_ref			

			file_path = os.path.join(reference_pop + "F_Mean_Patch" + processed_node_id + ".csv")
			filenames['female'].append(file_path)

			file_path = os.path.join(reference_pop + "M_Mean_Patch" + processed_node_id + ".csv")
			filenames['male'].append(file_path)

		# sum all the filepaths inside one cluster, then group by genotypes
		cluster_sum = monet.sumLandscapePopulationsFromFiles(filenames, male=maleToggle, female=femaleToggle, dataType=float)
		clusterGeno_sum = monet.aggregateGenotypesInNode(cluster_sum, aggregationDictionary)

		# take the difference between the sum and the clustered result
		# male
		male = str(agg_level) + "/" + str(run_id) + "/ANALYZED/E_0730_30_20_02_00020/M_Mean_Patch" + process_node_id(c) + ".csv"
		exp_path_M = os.path.join(experiments_path, male)
		# female
		female = str(agg_level) + "/" + str(run_id) + "/ANALYZED/E_0730_30_20_02_00020/F_Mean_Patch" + process_node_id(c) + ".csv"
		exp_path_F = os.path.join(experiments_path, female)

		filenames2 = dict()
		filenames2['male'] = [exp_path_M]
		filenames2['female'] = [exp_path_F]

		agg_sum = monet.sumLandscapePopulationsFromFiles(filenames2, male=maleToggle, female=femaleToggle)
		aggGeno_sum = monet.aggregateGenotypesInNode(agg_sum, aggregationDictionary)

		getDiff(aggGeno_sum, clusterGeno_sum, "agg_" + agg_level + "/cluster_" + process_node_id(c) + "/run_" + run_id + str(maleToggle) + str(femaleToggle))


def getDiff(aggGeno_sum, clusterGeno_sum, name):
	"""
	Takes path to cluster_id run in Experiments/,
	as well as the cluster_sum, which is the sum of all the nodes in that cluster_id.
	"""
	# print("AGG_GENO_RESULT: ", aggGeno_sum['population'].shape)
	# print("CLUSTER_GENO_RESULT: ", clusterGeno_sum['population'].shape)

	result = np.subtract(aggGeno_sum['population'], clusterGeno_sum['population'])

	with open(name + ".csv", mode="w") as cluster_summary:
		result_writer = csv.writer(cluster_summary)
		result_writer.writerow(population_IDs) # labels
		for r in result:
			result_writer.writerow(r)

def compareOnce():
	# sample randomly over runs provided
	print("Available keys are: ", counts.keys())
	for key in counts.keys():
		i = int(np.round(np.random.uniform(0, len(counts[key]) - 1)))
		run_path = key + "/" + counts[key][i]
		print("Running for key: ", key, " and run: ", counts[key][i])
		aggData = getAggregation(run_path, land_aggregated_path)
		cluster_run_sum = getSum(run_path, aggData)


## MAIN

## STEP 1: Create mapping from aggregated to not aggregated in csv

run_paths, counts = getExperimentPaths(experiments_path)

# STEP 2: Sum all nodes in a cluster and generate difference

for i in range(num_runs):
	compareOnce()

# run_dict = dict()
# for run_path in run_paths:
# 	run_dict[run_path] = getAggregation(run_path, land_aggregated_path)
# 	cluster_run_sum = getSum(run_path, run_dict[run_path])

# Previously used for testing, hardcoded
# key = 'C000250/Yorkeys01_0000_A' # 250 nodes, run 0
# run = run_dict[key] # dictionary for that run
# cluster_run_sum = getSum(key, run)
