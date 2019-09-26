# Threshold-Dependent Drives: Experiments' Analyses

Routines that perform the data analysis for the ["Confinement and reversibility of threshold-dependent gene drive systems in spatially-explicit Aedes aegypti populations"](https://www.biorxiv.org/content/10.1101/607267v1) paper.

##  Factorial Analysis

This workflow was created to calculate the response curves on the **releases number** and **batch migration events**, versus the **transgene** to **wild-type** ratio in a population across time.

1. Run the [factorialAnalysis.py](./factorialAnalysis.py) routine to get the factorial **CSV**. This file summarizes the response between two variables, and the change between **transgene** and **wild** population ratio across time.
    - This requires setting up the genotypes aggregation dictionary (**wildsList**, **homingList**) and calculating the ratios between them  (**ratiosDictionary**).
2. If the experiment presents a sensitivity analysis, run the [factorialDifferences.py](./factorialDifferences.py) script. This will generate a **CSV** that contains the information on the differences on the factorial slots against a baseline.
    - Needs an 'axis' file that presents the baseline behavior of the given scenario.
    - Uses a rescaling factor for the multiplication of _floats_.
3. Run the [TD_ResponseSurfaces.nb](./TD_ResponseSurfaces04.nb) script to export the curves that determine the **fixation/die-out** thresholds.


##  Population Dynamics

These are companion plots to do verify the behavior of the drives in terms of population dynamics.

* Run the [PopDyns.py](./PopDyns.py) script pointing towards the path where the mean behavior results are stored.
