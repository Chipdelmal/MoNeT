1. getexperimentPaths(creates mapping aggregated to non-aggregated)
    a. This yields run_paths (all run paths), and counts (a dictionary where the key    is agg_path, and the value is a list of run_paths)
2. compareOnce currently gets called once:
    a. for each aggregation level (counts.keys()), samples randomly over all runs to    produce a run_path
    b. Call getAggregation() on that run_path, and land_aggregated_path
            run_path: the path specifying a level of aggregation, and a runID
            land_aggregated_path: the path to the LandAggregated folder, holding cluster summaries
        Returns a dictionary agg_data[clusterID] = [nodeIDs that were aggregated into this cluster] 
        Also saves a CSV file with the results. 
    c. Call getSum() on that run_path, and agg_data
            key (run_path) tells us the level of aggregation, and a runID
            run (agg_data) is a dictionary agg_data[clusterID] = [nodeIDs that were aggregated into this cluster]
        for each clusterID:
            for each nodeID aggregated into this cluster:
                    * file_path uses reference_pop, because it's where we expect to find all the nodeIDs available for summation. 
                retrieve the matrices for that nodeID
            aggregate all the nodes into aggGeno_sum, clusterGeno_sum
            call getDiff() on aggGeno_sum, clusterGeno_sum, name
                takes the difference between aggGeno_sum['population] and clusterGeno_sum['population]
                writes the difference in time series format to csv
            

reference_pop = "/Users/gillian/Desktop/GillianDataset/Experiments/C002195/Yorkeys01_0027_A/ANALYZED/E_0730_30_20_02_00020/"

This hardcoded the run ID: Yorkeys01_0027_A
