---
title: MoNeT (Mosquito Networks Taskforce)
layout: default
---

This idea was born to facilitate collaboration in network analysis routines useful for both [*MGDrivE*](https://marshalllab.github.io/MGDrivE/) (__UC, Berkeley__) and [*MASH*](https://smitdave.github.io/MASH-Main/) (__IHME__) projects. Its main objective is to create a set of tools that allow us to study landscapes in a way that is relevant in terms of mosquito-borne diseases.

Additionally, this project's reach has been extended to facilitate the collaboration between the core [*MGDrivE*](https://chipdelmal.github.io/MGDrivE/) development team (__UC, Berkeley__), and faculty at __Tecnológico de Monterrey__ with the objective of getting computer science undergraduate students in México involved in mosquito-borne diseases research projects.

<hr>

# Description

When this project started, it was mainly aimed at using network theory to understand the transmission of pathogens and the spread of gene-drives in spatial settings, however, the scope of the project was extended to the development of computational toolkits that can aid in the elimination of mosquito-transmitted diseases.

<img src="./media/MoroniPoint.jpg" width="50%" align="middle"><img src="./media/MoroniHex.jpg" width="50%" align="middle">

<hr>

# Workflows

__Click on the titles for more information.__


## [Mosquito Sinks and Sources Detection](./SinkSource.html)

Mosquito-flow in the landscape is defined by the biological needs of the insects and the availability of resources (in a simple scenario). In certain situations, these variables might generate structures where mosquitos flows are highly directional between geographical clusters. This workflow was created to investigate which properties of the landscapes give birth to these kind of dynamics.

<img src="./media/npartite.jpg" width="100%" align="middle">

## [Targeted Interventions](./TargetedInterventions.html) and [Regular Grid Markov Analysis](./TheWalkingDead.html)

Identifying the most important points in landscapes in terms of mosquito-control interventions' effectiveness is far from a trivial task. These individuals move in probabilistic patterns according to their intrinsic biological needs, and environmental factors. To maximize the effect of the deployed measures to kill them, we need to take into account these variables, and this is what this workflow is all about.

<img src="./media/00_clustering.jpg" width="50%" align="middle"><img src="./media/03_MarkovStationary.jpg" width="50%" align="middle">

## [Centrality Analysis of Landscapes](./Centrality.html)

The study of gene-drives' spread in realistic landscapes is of upmost importance when we think of using them to eradicate mosquito-borne diseases. Given that the insects' movements are the driving force behind these genes' spread, studying the flow of these individuals in geographic settings becomes crucial. In this workflow we borrow the centrality analysis of networks to understand the nodes that are more relevant in terms of these patterns, so that we can use this information to design studies that allow us to confine our constructs to designated areas.

<img src="./media/YorkeysKnob_centralityHex.jpg" width="50%" align="middle"><img src="./media/YorkeysKnob_centralityScatter.jpg" width="50%" align="middle">

## [Clustering of Directed Networks with Geographical Constraints](./Community.html)

Targeted vector control interventions are usually applied on the field without taking into account the movement of mosquitos across the landscape. This, however, might not be the most optimal way of trying to eradicate these insects. In this workflow, we try to create and test a clustering algorithm that takes into account both: mosquito movement, and geographical constraints; to understand the factors that would promote more efficient mosquito-control campaigns.

<img src="./media/headerImage.jpg" width="100%" align="middle">

## [Landscape Aggregation](./LandscapeAggregation.html)

Simulating landscapes in extreme resolution requires a lot of computational resources, however, aggregating the spatial units in naive ways might lead us to lose crucial information about the spatio-temporal processes that we want to study. In this workflow we explore how different levels of clustering affect the information we obtain on the dynamics of gene flows in spatial settings (with the use of the [*MGDrivE*](https://marshalllab.github.io/MGDrivE/) framework).

<img src="./media/E_080_000_000_000-04 (1).png" width="100%" align="middle">

## [Gene Drives Visualizations Tools](./DataVisualization.html)

The [*MGDrivE*](https://marshalllab.github.io/MGDrivE/) project has presented interesting challenges in terms of data analysis and visualization. By using _Mathematica_ and _Python_ we have been compiling a toolkit of plots and routines that allow us to analyse and describe the way genes disperse in the enviornment as a consequence of mosquito movement.

<img src="./media/SpheresPlots_H.jpg" width="100%" align="middle">

## [Mosquito App](./MosquitoApp.html)

This project was developed at "Tecnológico de Monterrey" as part of a collaboration with UC, Berkeley. The aim of the project was to develop a mobile application that was able to capture mosquito sightings with the following information: mosquito photograph, geo-location of the sighting, temperature, and humidity. This information is to be used by research teams to build databases of mosquito presence across different landscapes.

<img src="./media/appDemo.png" width="100%" align="middle">


## [Tools for Fighting Malaria and Other Mosquito Borne Diseases](./ToolsCollaboration.html)

This workflow was created to facilitate the creation of tools to be used as part of the [*MGDrivE*](https://marshalllab.github.io/MGDrivE/) project. It represents the collaboration between UC, Berkeley and Tecnológico de Monterrey in an effort to get undergraduate students involved in mosquito-borne diseases research projects.

<img src="./media/stillFlow.png" width="100%" align="middle">


<!--
## [Pointsets Generation](./Pointsets.html)

Even though we can parse real-world landscapes from OpenStreet Map, generating random points distributions is still useful in terms of theoretical questions about how these distributions affect the metrics and results of our analyses.
-->

<!-- ## Road-Flight Path Intersections

<i>Aedes aegypti</i>  mosquitos avoid flying over roads; which, in turn, modifies the expected movement flows on the landscape. We would like to study how this specific variable affects the broad-scale dynamics of mosquito movement to understand the effects this would have in diseases transmission; but for now this is still an open line to be tackled. -->


## [Households Distances Analysis](./HouseholdDistances.html)

The distance between households is thought to be an important metric in terms of the analysis of mosquito populations mixing and gene-drive flow. This is particularly true in the case of the _Aedes aegypti_ species, which is know for being a weak flyer that lives in close vicinity to human houses. This auxiliary workflow is aimed towards calculating the distances between the centroids of the households so that we can characterize the impact of these distances in terms of gene-flows.

<hr>

# Other Workflows and Scripts

* [Useful Network Metrics](./NetworkMetrics.html): This document contains some of the notes we have compiled on the networks metrics that could provide some insights of how mosquito movement shapes the transmission of both: diseases and gene drives.
* [Python Package](./PythonModule.html): A compilation of the functions created as part of the project.
* [Conda Environment](./CondaEnvironment.html): The environment that contains all the packages required to run our routines.
* [OSMnx Parser](./OSMnx.html): A script to parse and export SHP files from buildings roads polygons from [Open Street Map](https://www.openstreetmap.org/#map=14/-11.7114/43.2587) using [OSMnx](https://github.com/gboeing/osmnx).
* [Fancy Maps Parser](./FancyMaps.html): A _Mathematica_ script that parses maps from _Wolfram Database_, exports the coordinates, populations, and a "fancy" map.

<!--<center>
<img src="./media/France.jpg" width="33%" align="middle"><img src="./media/Madagascar.jpg" width="33%" align="middle"><img src="./media/Italy.jpg" width="33%" align="middle">
</center>-->

<hr>

# Authors

<ul style="font-size:12.5px">
  <li>Lead: <a href="https://chipdelmal.github.io/">Héctor M. Sánchez C.</a> [UCB]</li>
  <li>Dev: Sarafina Smith  [UCB], <a href="https://www.linkedin.com/in/biyonkaliang">Biyonka Liang</a> [UCB], Gillian Chu [UCB], Victor Ferman [UCB], <a href="https://slwu89.github.io/">Sean L. Wu</a> [UCB]</li>
  <li>Collaborators: <a href="https://www.researchgate.net/profile/Benjamin_Valdes">Benjamín Valdés</a> [ITESM], András Takacs  [ITESM]</li>
  <li>PI's: <a href="http://sph.berkeley.edu/john-marshall">John M. Marshall</a> [UCB] and <a href="http://www.healthdata.org/about/david-smith">David L. Smith</a> [IHME]</li>
</ul>


<ul style="font-size:12.5px">
  <li>Former dev: Sabrina Wong [UCB]</li>
</ul>

<hr>

<center>
<img src="./media/berkeleyLogo.jpg" height="60px"><img src="./media/ihmeLogo.jpg" height="60px"><img src="./media/itesm.png" height="75px">
</center>
