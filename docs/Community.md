## Clustering of Directed Networks with Geographical Constraints

The main idea for this workflow is to create an algorithm that combines the information of the geographical clustering of a pointset, along with the mosquito movement kernel. The advantage of doing this, would be that it would take into account the mosquito movement part of the dynamics of the disease transmission, while still making it aware that these dynamics are "anchored" to a geographic setting; giving us an informed way to aggregate geographic populations of mosquitos moving on the landscape.

**IMPORTANT NOTE:** This work is being carried out by [Biyonka Liang](https://github.com/biyonka) as part of her undergraduate thesis, so a complete description of the algorithm will be published once this document is available.

## Why?

There's several reasons why we could be interested in performing this constrained clustering. Our two main drivers, in the case of mosquito-borne diseases field are:
* To cluster mosquito-movement into specific geographies that are constrained by weather, or behavioral similarities. We could consider clusters to be homogeneous in their "within" behavior.
* To plan mosquito-control interventions wherever mosquito movement is not easily approximated by diffusion.

## Geographical Penalty on Movement Kernel

We calculate the clustering using the [InfoMap](http://www.mapequation.org/code.html) algorithm, by using the mosquito movement kernel (which is, in turn, calculated with information of how mosquitos move probabilistically across the landscape); but, whilst doing so, we add a geographic penalty by calculating either the total Euclidean distance between points, the distances to the medioids, etcetera.

## Status

This is an ongoing project with its own [repository](https://github.com/biyonka/malarialnetworks), so we will be updating information as the code becomes more stable and tested.

## Authors

Biyonka Liang, Héctor M. Sánchez C., Sean L. Wu, John M. Marshall, David L. Smith
