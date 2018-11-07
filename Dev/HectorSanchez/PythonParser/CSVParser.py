import os
import glob
import numpy as np

import pythonParser as pyPar


# User Input
path="/Users/sanchez.hmsc/Desktop/ParserDataset/E_080_000_000_000";
sexFilenameIdentifiers={"male":"ADM","female":"AF1"}
stochastic=False
nodeIndex=1




# Read filenames (assumes lexicographycal order is consistent across male, and female patches)
filenames=os.listdir(path)
maleFiles=sorted(glob.glob(path + "/" + sexIdentifiers.get("male") + "*.csv"));
femaleFiles=sorted(glob.glob(path + "/" + sexIdentifiers.get("female") + "*.csv"));

#
tempFileM=maleFiles[nodeIndex]
tempFileF=femaleFiles[nodeIndex]

# Load male and female data
dataType=int;
if (stochastic==False):
    dataType=float;
dataM=np.genfromtxt(tempFileM,dtype=dataType,skip_header=1,delimiter=",")
dataF=np.genfromtxt(tempFileF,dtype=dataType,skip_header=1,delimiter=",")
dataA + dataB



#help(np.zeros_like);
#help(np.genfromtxt);

type(filenames)
filenames

help(readExperimentFilenames)
