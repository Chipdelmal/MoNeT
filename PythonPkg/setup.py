from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(
    name='MoNeT_MGDrivE',
    version='0.4.3',
    url='https://chipdelmal.github.io/MoNeT/',
    author='Hector M. Sanchez C.',
    author_email='sanchez.hmsc@berkeley.edu',
    description="MoNeT python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy', 'scipy', 'matplotlib',
                      'ipython', 'jupyter', 'pandas', 'sympy'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
 )
