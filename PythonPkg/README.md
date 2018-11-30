# MoNeT Python Package

To upgrade the package, change the version number in setup.py and run the following:

python3 setup.py sdist bdist_wheel

python -m twine upload dist/*
