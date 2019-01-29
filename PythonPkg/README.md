# MoNeT Python Package

## To update online

View the package at https://pypi.org/project/MoNeT-MGDrivE/

To upgrade the package, change the version number in setup.py and run the following:

```bash
python3 setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## To update locally

Move into the **PythonPkg** folder and run:

```bash
pip install .
```

To install in the *Conda Environment*:

```bash
source activate MoNeT
pip install .
```
