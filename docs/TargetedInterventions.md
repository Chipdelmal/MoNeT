## Targeted Interventions

### Brief Description

As mentioned before, to make the most efficient use of our mosquito-control interventions, we need to make an analysis that takes into account not only the geographic distribution of households in the environment, but also the biological needs of the mosquitoes as they move through it.

To do so, we start by laying out our simulated landscape:

<img src="./media/00_clustering.jpg" width="100%" align="middle">

Once that is done, we can assign _n_ number of classes to simulate the different types of habitats. This can be done by defining an _n_-partite space for the network, where _n_ is the number of types of nodes, and the strength of the directionality defines the "partite-ness" of the connections (one a fully partite network and 0.5 equal to having each type of node being equally probable regardless of its class).

For this example, we will simulate two types of nodes (_n=2_) as shown in the figure that follows:

<img src="./media/01_Movement.jpg" width="100%" align="middle">

This results in an _n_-dimensional network in which mosquitoes move. If we think of mosquitoes as being simplified to random walkers in the network, we can reduce their movement to a Markov process in which their next step depends on their current location (assuming they have fulfilled their biological need). With this information, we can calculate the steady-state distribution of the nodes:

<img src="./media/04_markovSteady.jpg" width="100%" align="middle">

And, to visualize this better, we can rescale our network to highlight the nodes in which our random-walking mosquitoes spend more time (the ones to which they jump more often):

<img src="./media/03_MarkovStationary.jpg" width="100%" align="middle">

This is confirmed by running random walkers on top of our transitions network:

<img src="./media/05_markovSteady2.jpg" width="100%" align="middle">

This analysis can be elevated to arbitrarily high dimensions of point types, and more flexible transition probabilities between classes (less partite-ness):

<img src="./media/00_clustering2.jpg" width="50%" align="middle"><img src="./media/03_MarkovStationary2.jpg" width="50%" align="middle">

### Next Steps

The natural next step for this workflow would be to simulate mosquitoes on the network, and compare the death rates of applying in different random and targeted schemes.

### Authors

Héctor M. Sánchez C., Biyonka Liang, Sean L. Wu, Daniel Citron, David L. Smith
