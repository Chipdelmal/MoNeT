# Aggregation Routines

##  Aggregation Workflow

1. Run [sortLatLongsByDistance](./sortLatLongsByDistance.py) to get a more reasonable ordering on the nodes.
2. Run [calculateDistanceAndMigration](./calculateDistanceAndMigration.py) to generate the distances and migration matrix.
3. Run [clusterAndAggregate](./clusterAndAggregate.py) to do the aggregation at the necessary levels, and at the repetitions needed.
4. Run [sampleReleases](./sampleReleases.py) to generate the random sampling of the nodes to release gene-drive mosquitos.
5. Run [mapCluster](./mapClusters.py) to export plots on the clusters as a basic means of verification.

##  Key

* *S*: Sorted
* *D*: Distance
* *M*: Migration
* *A*: Aggregated
* *I*: Aggregated with clusters IDs and centroids
* *R*: Releases


##  Analysis Workflow

1. Run [errorMetric](./errorMetric.py) to compute the mean responses across experiments, along with the standard deviation and median (the stats metrics can be changed if needed).
2. Run [errorVerification](./errorVerification.py) to export plots of the aggregation responses.
