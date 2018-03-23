---
title: MoNeT: Mosquito Networks Taskforce
layout: default
---

# Mosquito Networks Taskforce

This repository was created to facilitate collaboration in network analysis routines useful for both *MGDrivE* and *MASH* projects. Its main objective is to create a set of tools that allow us to study landscapes in a way that is relevant in terms of mosquito-borne diseases.

<img src="./media/npartite.jpg" width="100%" align="middle">

## Description

Mosquito movement across landscapes can be approximately modeled by transition probabilities that are defined by the distances between resources points in a spatial plane. This is because mosquitoes move from point to point in search of resources and to fulfill biological needs. Taking this into account, it makes sense to think of this landscape as a network of resources, where the mosquito movement is directed between sites.

<img src="./media/MoroniPoint.jpg" width="50%" align="middle"><img src="./Media/MoroniHex.jpg" width="50%" align="middle">

## Workflows

The broad-scope of the project has been divided into several workflows that follow the over-arching theme of analyzing mosquito movement in geographic point sets.

### [Mosquito Sinks and Sources Detection](./SinkSource.html)

Mosquito-flow in the landscape is defined by the biological needs of the insects and the availability of resources (in a simple scenario). In certain situations, these variables might generate structures where mosquitos flows are highly directional between geographical clusters. This workflow was created to investigate which properties of the landscapes give birth to these kind of dynamics.

### [Clustering of Directed Networks with Geographical Constraints](./Community.html)

Targeted vector control interventions are usually applied on the field without taking into account the movement of mosquitos across the landscape. This, however, might not be the most optimal way of trying to eradicate these insects. In this workflow, we try to create and test a clustering algorithm that takes into account both: mosquito movement, and geographical constraints; to understand the factors that would promote more efficient mosquito-control campaigns.

<!--Authors: Biyonka Liang, Héctor M. Sánchez C., Sean L. Wu, Daniel Citron, John M. Marshall, David L. Smith-->
### [Centrality Analysis of Landscapes](./Centrality.html)


### Road-Flight Path Intersections

## Auxiliary Scripts and Libraries

### [OSMnx Parser](./OSMnx.html)

### [Python Module](./PythonModule.html)

### [Conda Environment](./CondaEnvironment.html)


## Authors

<a href="https://chipdelmal.github.io/">Héctor M. Sánchez C.</a>, <a href="https://slwu89.github.io/">Sean L. Wu</a>, Biyonka Liang, Sarafina Smith, Sabrina Wong<br>

## PI's

John M. Marshall and David L. Smith
