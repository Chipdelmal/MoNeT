# Configuring MGDrivE

[![N|Solid](https://marshalllab.github.io/MGDrivE/images/logo.png)](https://marshalllab.github.io/MGDrivE/images/logo.png)

MGDrivE is a framework designed to serve as a testbed in which gene-drive releases for mosquito-borne diseases control can be tested. It is being developed to accommodate various mosquito-specific gene drive systems within a population dynamics model that allows migration of individuals between nodes in a spatial landscape.

# Installation
#### Download all the dependencies
- Matplotlib
- NumPy
- Pandas
- compress-pickle
```
python -m pip install -U pip
pip install -U matplotlib numpy pandas compress-pickle
```
- Basemap
Download Anaconda first: https://docs.anaconda.com/anaconda/install/
After you install Anaconda:
```
conda install -c anaconda basemap
```
#### Getting MGDrivE
```
pip install MoNeT-MGDrivE
python
import MoNeT_MGDrivE
exit()
```
#### OPTION 1: Setting Up and Using Anaconda Environment
```
conda create -n MoNeT python=3.8
conda activate MoNeT
conda install -c anaconda basemap
pip install jupyter #Optional
pip install MoNeT_MGDrivE
onda deactivate
```
Now, your prompt will go from (base)USERNAME: ~ to (MoNeT)USERNAME: ~

#### OPTION 2: Using a Virtual Environment
Only drawback with this method is that it does not have a conda workaround for BaseMap, so can be a bit more complicated to install that dependency.
```
virtualenv env/dataPy
virtualenv --relocatable env/dataPy
source env/dataPy/bin/activate
pip install MoNeT_MGDrivE
```
# Using MGDrivE
Now, anytime you need to use MGDrivE, you can simply use the following commands:
```
conda activate MoNeT
jupyter notebook
#Create an .ipynb and conduct data analysis
conda deactivate
```
And now you are done! 🎉🎉
