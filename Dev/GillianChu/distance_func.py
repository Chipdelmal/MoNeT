from distutils.core import setup
from Cython.Build import cythonize

setup(
	ext_modules = cythonize("/Users/gillian/Desktop/marshall/MGDrivE/MGDrivE/src/MGDrivE-DistanceFunctions.cpp")
)