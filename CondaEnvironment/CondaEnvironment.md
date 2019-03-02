
## Installation Instructions

To install the *conda* environment run the following command in terminal (requires _Anaconda_):

```bash
conda env create -f MoNeT.yml -n MoNeT
```

To run the environment:

```bash
source activate MoNeT
```

To close the environment:

```bash
source deactivate
```

Adding the environment to Hydrogen (in atom):

```bash
source activate MoNeT
python -m ipykernel install --user --name MoNeT
```

## Other Notes

To install *Miniconda*:

```bash
sh Miniconda3.sh
```

To export environment to *YML* (after activating):

```bash
conda env export > MoNeT.yml
```

To install ipykernel in hydrogen (to run notebooks in "Jupyter" style from atom):

```bash
python -m pip install ipykernel
python -m ipykernel install --user
```

To load MoNeT as a kernel in Jupyter and Hydrogen:

```bash
source activate MoNeT
python -m ipykernel install --user --name MoNeT --display-name "Python (MoNeT)"
```

To remove MoNeT from the Jupyter kernel list:

```bash
jupyter kernelspec list
jupyter kernelspec uninstall MoNeT
```

<hr>

## Authors

Héctor M. Sánchez C.
