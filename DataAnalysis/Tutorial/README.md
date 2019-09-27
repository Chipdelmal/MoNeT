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

Although not critical, we then define the style constants that will be used for our plots throughout the script. Our package takes `#HEX`-coded color entries.

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
