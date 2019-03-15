# MoNeT Python Package


## To update locally (in the Conda environment)

Move into the **PythonPkg** folder and run:

```bash
pip install .
```

To install in the *Conda Environment*:

```bash
source activate MoNeT
pip install .
source deactivate
```

## To update the package at PyPi (for code maintainer)

View the package at https://pypi.org/project/MoNeT-MGDrivE/

To upgrade the package, change the version number in setup.py and run the following:

```bash
python3 setup.py sdist bdist_wheel
twine check dist/*
python -m twine upload dist/MoNeT_MGDrivE-0.4.5.2.tar.gz --skip-existing
```

Updating the package in TestPypi

```bash
python3 setup.py sdist bdist_wheel
twine check dist/*
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/MoNeT_MGDrivE-0.4.5.2.tar.gz  --skip-existing
```
