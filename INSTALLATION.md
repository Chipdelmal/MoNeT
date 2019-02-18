# Python Installation Instructions

To install the required libraries and packages follow these steps:

##  1. Clone the git repository

```bash
git clone https://github.com/Chipdelmal/MoNeT.git MoNeT
```

##  2. Install Anaconda and Python 3.7

Download and install [Anaconda](https://www.anaconda.com/) and [Python 3.7](https://www.python.org/downloads/release/python-370/) following the instructions provided in their websites.

##  3. Install or create the "Conda" environment

### a. Installing from the YML image

In the terminal, move to the **./CondaEnvironment/** directory and run the following command:

```bash
conda env create -f MoNeT.yml -n MoNeT
```
### b. Creating the image from scratch

Run the following line on the terminal to create the environment:

```bash
conda create -n MoNeT python=3.7
```

And, to install the required dependencies, run:

```bash
source activate MoNeT
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install plotly
source deactivate
```


### Optional: Loading the environment in Jupyter/Hydrogen

In case you want to have the image loaded as a kernel in [Jupyter](https://jupyter.org/) or [Hydrogen (atom)](https://atom.io/packages/hydrogen), run:

```bash
source activate MoNeT
python -m ipykernel install --user --name MoNeT --display-name "MoNeT"
source deactivate
```

For more information on how to install and setup [Hydrogen](https://atom.io/packages/hydrogen) to run in-line python within atom follow this [link](https://jstaf.github.io/2018/03/25/atom-ide.html).


##  4. Install the "MoNeT_MGDrivE" python package

Finally, to install the [Python](https://www.python.org/downloads/release/python-370/) package to perform the analyses required by [MGDrivE](https://marshalllab.github.io/MGDrivE/) model, move into the **./PythonPkg/** and run:

```bash
source activate
pip install .
source deactivate
```
