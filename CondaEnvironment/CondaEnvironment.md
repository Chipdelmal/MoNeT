
## Installation Instructions

To install the *conda* environment containing: _iGraph_, _NetworkX_, _PlotLy_  and _SciKit_; run the following command in terminal (requires _Anaconda_):

```
conda env create -f MoNeT.yml -n MoNeT
```

To run the environment:

```
source activate MoNeT
```

To close the environment:

```
source deactivate
```

Adding the environment to Hydrogen (in atom):

```
source activate MoNeT
python -m ipykernel install --user --name MoNeT
```

## Other Notes

To install *Miniconda*:

```
sh Miniconda3.sh
```

To export environment to *YML* (after activating):

```
conda env export > MoNeT.yml
```

To install ipykernel in hydrogen (to run notebooks in "Jupyter" style from atom):

```
python -m pip install ipykernel
python -m ipykernel install --user
```

To load MoNeT as a kernel in jupyter kernel in Hydrogen:

```
source activate MoNeT
python -m ipykernel install --user --name MoNeT --display-name "Python (MoNeT)"
```

<hr>

## Authors

Héctor M. Sánchez C.
