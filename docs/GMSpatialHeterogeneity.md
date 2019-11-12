##  Habitat Heterogeneity Effects on the Spread of Gene Drives

Spatial heterogeneity is widely known to be important for the study of mosquito-borne diseases. However, it has rarely been studied in a systematic way. With the advent of gene-drive systems, the need for understanding of heterogeneity has become important due to the impact it could have in the prediction and confinability of these constructs in the field.

Our research group at University of California, Berkeley has developed a model to simulate spatiotemporal releases of mosquito gene-drives in arbitrary landscapes: [MGDrivE](https://marshalllab.github.io/MGDrivE/). In this framework we can run controlled experiments of realistic spread of genetic constructs so it makes sense for us to make use of it to simulate and analyze how the genetic modifications spread in landscapes with varying degrees of heterogeneity.

<!--(starting with the [MCR](http://science.sciencemag.org/content/348/6233/442))-->

To do so, we plan to take the following steps (click on the titles for more information):

### 0) Baseline landscape

We will start our analysis in a one-dimensional landscape. Across our experiments, we will use a line with **n** nodes in which each habitat will have a population size of: **p/n**. Where **p** is the total amount of male and female mosquitos in the environment. These nodes will be separated by a distance **d**, which needs to be calibrated according to the mosquito species under study (in this case, the *Aedes aegypti* mosquito).

<img src="./media/habitat00.png" width="100%" align="middle">

### 1) [Spatial Distribution (Biyonka Liang)](./SpatialDistribution.html)

The first dimension of heterogeneity we will look into is the spatial distribution of mosquito breeding sites. To do this, we will randomly select **m** nodes in our baseline landscape, and shift them with a Gaussian probability kernel centered in the nodes' initial locations.

<img src="./media/habitat02.png" width="100%" align="middle">

### 2) [Population Distribution (Maya Shen)](./PopSizeHeterogeneity.html)

The second dimension of variation we intend to study is the distribution of the population across breeding sites. Our initial systematic approach to doing it is to take the total population **p** and re distribute it randomly through the breeding sites.

<img src="./media/habitat01.png" width="100%" align="middle">

### 3) [Levels of Aggregation (Gillian Chu)](./LandscapeAggregation.html)

Additionally, understanding the level of abstraction in the resolution of landscapes that can be tolerated for a particular analysis is extremely important. This is because we are ultimately constrained by computational resources, so we need to have a clear image of how much information is being lost when we aggregate breeding sites by mixing their populations to allow us the simulation of larger landscapes.

<img src="./media/habitat03.png" width="100%" align="middle">


### 4) [Point-Type Heterogeneity (Yunewn Ji)](./PointType.html)

Another point of interest in these studies is how the availability of resources affects the way mosquitos move across the landscape. For this, we are setting up landscapes with heterogeneous pointsets to understand the impact of resources locations in mosquito flows.

<!-- ### 4) Factorial Combinations

Finally, once our routines have been tested independently, we will perform factorial combination experiments and data analysis to look for non-linear interactions of the heterogeneity components in an effort to enhance our understanding of these complex processes and to optimize our use of resources when performing gene-drive releases in the field.

<center><img src="./media/habitat04.png" width="60%" align="middle"></center> -->


### Authors

* **Lead:** Héctor M. Sánchez C.
* **Dev/Research:** Gillian Chu, Maya Shen, Yunwen Ji, Biyonka Liang*, Sarafina Smith*
* **PI:** John M. Marshall
