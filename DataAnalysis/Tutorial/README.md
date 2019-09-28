# Tutorial and Template

These scripts have examples of the most common uses for gene-drives spatiotemporal analyses within the lab (using the [MoNeT-MGDrivE python package](https://pypi.org/project/MoNeT-MGDrivE/)).


##  Installation

It is highly recommended to create an [Anaconda](https://www.anaconda.com/distribution/) environment to keep the packages installations clean and independent. To do so, install either [anaconda3](https://www.anaconda.com/distribution/#download-section) or [miniconda3](https://docs.conda.io/en/latest/miniconda.html) and follow these instructions.

### Creating the environment

To install [MoNeT_MGDrivE](), we require additional dependencies to be installed. In our []() releases repository, we do provide [YML](https://github.com/Chipdelmal/MoNeT_MGDrivE/blob/master/conda/MoNeT.yml) and [TXT](https://github.com/Chipdelmal/MoNeT_MGDrivE/blob/master/conda/MoNeT.txt) files to automatically create the environment with the required dependencies with either of the following commands:

```bash
# From YML file:
conda env create -f MoNeT.yml -n MoNeT
# From TXT file:
conda create -n new MoNeT --file REQUIREMENTS.txt
```

We have found this, however, to be unreliable due to OS incompatibilities, so we provide the instructions to create the environment from scratch:

```bash
# Create an empty environment running on Python 3.7
conda create -n MoNeT python=3.7
# Installing dependencies
conda activate MoNeT
pip install numpy matplotlib scipy jupyter pandas
conda install -c anaconda basemap
conda deactivate
```

Now that we've installed all the required dependencies, we can work by running:

```bash
# To activate our environment:
conda activate MoNeT
# [Work and run scripts]
python script.py
# To deactivate:
conda deactivate
```

##  Dataset

The datasets used for this demo can be found at the lab's shared drive in the following path:

```bash
/Volumes/marshallShare/MGDrivE_Datasets/Tutorial/
```

These simulation results show an ERACR drive spreading in the **Yorkeys Knob & Trinity Park** landscape at three levels of aggregation.

##  Tutorial

### Setting Everything Up

We start, as always, by loading our libraries.

```python
import glob
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
```

Most of the time, we define a `ROOT PATH` for the experiments, that we keep as a base for reading experiments **CSVs** and exporting **plots/summary statistics**. The experiment name is important for files export consistency. Finally, we setup the bool flags that determine if we're analyzing **male** and/or **female** mosquito counts (which is relevant to understand releases schemes).

```python
EXP_NAME = 'C2195'
PATH_ROOT = '/Volumes/marshallShare/MGDrivE_Datasets/Tutorial/'
(maleToggle, femaleToggle) = (True, True)
```

Although not critical, we then define the style constants that will be used for our plots throughout the script. Our package takes `#HEX`-coded color entries. The `cmaps` for the spatial heatmaps can also be generated automatically (this will be clearer when the spatial analysis part is presented).

```python
colors = ['#2d2275', '#fc074f', '#ccf70c', '#3399ff']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
style = {
    "width": .05,  "aspect": .01, "dpi": 1024, "legend": False,
    "alpha": 1, "colors": colors,
    "xRange": [0,1000], "yRange": [0,100000]
}
```

Now, we can start defining the `aggregationDictionary` that sets-up how the genotypes counts will be aggregated. The way this works is by taking a list of the **genotype tags** (names), and a list of lists that denote which columns in the **CSV** files contain the desired genotype to be counted. These lists can have repeated indices for "double-counting" genes in a particular locus (**EE**, for example, would require counting the column twice to get the **E** gene correctly accounted for).


```python
# Population CSV Header: [WW, WH, WE, WR, WB, HH, HE, HR, HB, EE, ER, EB, RR, RB, BB]
aggregationDictionary = {
    'genotypes': ['W', 'H', 'E', 'R'],
    'indices': [
        [0, 0, 1, 2, 3, 4],
        [1, 5, 5, 6, 7, 8],
        [2, 6, 9, 9, 10, 11],
        [3, 7, 10, 12, 12, 13, 4, 8, 11, 13, 14, 14]
    ]
}
```

In this example we are aggregating the **R** and **B** genes into the same counting category.

### Aggregated Mean Response

Loading the files in a correct way is highly experiment-dependent, but we provide with as many helper functions as possible to make it seamless. If necessary, however, paths to files can always be accessed with `glob`. In the specific case of these experiments, we have a nested folder within the **ANALYZED** folder: `./C0025/ANALYZED/E_0730_30_20_02_00020 `, so we access the folder to get all the experiment files stored within it:

```python
# Base ANALYZED folder
folderMean = PATH_ROOT  + EXP_NAME + '/ANALYZED/'
# Getting the paths for all the experiments files in the inner folder
innerFolder = monet.listDirectoriesInPath(folderMean)[0]
filenames = monet.readExperimentFilenames(folderMean + innerFolder)
```

With the paths correctly loaded, we can now sum our whole landscape into one population count, and then aggregate the counts by genotype:

```python
# Load and aggregate the whole landscape into a population count
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=maleToggle, female=femaleToggle
)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData, aggregationDictionary
)
```

Finally, we can plot the `stack` of the genotypes distribution for further analysis:

```python
figStack = monet.plotMeanGenotypeStack(
    aggData, style
)
figStack.get_axes()[0].set_xlim(style["xRange"][0], style["xRange"][1])
figStack.get_axes()[0].set_ylim(style["yRange"][0], style["yRange"][1])
monet.quickSaveFigure(
    figStack, PATH_ROOT + "S_" + EXP_NAME + ".png"
)
plt.close()
```

### Spatiotemporal Response

The second type of analysis we will show is the spatiotemporal response...

```python
# Get the filenames for a particular experiment in the ANALYZED folder
folderMean = PATH_ROOT  + EXP_NAME + '/ANALYZED/'
# Getting the paths for all the experiments files in the inner folder
innerFolder = monet.listDirectoriesInPath(folderMean)[0]
filenames = monet.readExperimentFilenames(folderMean + innerFolder)
```

Once again, we process these files by aggregating them but this time, we don't sum the whole landscape into the same count:

```python
# Process landscape data
landscapeData = monet.loadLandscapeData(
    filenames, male=maleToggle, female=femaleToggle
 )
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData, aggregationDictionary
)
```

This time, we need a bit more processing. After aggregating the landscape by genotypes, we need to generate spatiotemporal arrays to be able to process the information, along with their normalized version (in case the population sizes are heterogeneous):

```python
# Calculate the 
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)
# Rescale the nodes on a relative "maxPop" instead of landscape-wide
geneSpatiotemporalsNorm = monet.rescaleGeneSpatiotemporals(geneSpatiotemporals)
```

```python
# Plot the populations heatmap
(nodes, maxTime) = geneSpatiotemporals['geneLandscape'][0].shape
maxPop = monet.maxAlleleInLandscape(geneSpatiotemporals["geneLandscape"])
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporalsNorm,
    style={"aspect": maxTime/nodes * .1, "cmap": cmaps},
    vmax=1
)
monet.quickSaveFigure(
    overlay, PATH_ROOT + "O_" + EXP_NAME + ".png"
)
plt.close()
```
