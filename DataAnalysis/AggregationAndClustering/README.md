# Aggregation routines instructions

##  Workflow

1. Run [sortLatLongsByDistance](https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/AggregationAndClustering/sortLatLongsByDistance.py) to get a more reasonable ordering on the nodes.
2. Run [calculateDistanceAndMigration](https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/AggregationAndClustering/calculateDistanceAndMigration.py) to generate the distances and migration matrix.
3. Run [clusterAndAggregate](https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/AggregationAndClustering/clusterAndAggregate.py) to do the aggregation at the necessary levels, and at the repetitions needed.

##  Key

* S: Sorted
* D: Distance
* M: Migration
* A: Aggregated
* I: Aggregated with clusters IDs and centroids
* R: Releases
