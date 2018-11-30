import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	  name='MoNeT_MGDrivE',
      version='0.2.1',
      url='https://github.com/Chipdelmal/MoNeT',
      author='Hector M. Sanchez C.',
      author_email='sanchez.hmsc@berkeley.edu',
      description="MoNeT python package",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      install_requires=['numpy'],
      license='MIT',
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
      ],
 )
