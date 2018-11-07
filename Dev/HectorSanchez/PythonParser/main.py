import os
import glob
import numpy as np

import experimentsParser as exPar


# Define the experiment's path
path="/Users/sanchez.hmsc/Desktop/ParserDataset/E_080_000_000_000";

# Get the filenames lists
filenames=exPar.readExperimentFilenames(path)

# Load a single node
nodeIndex=0
nodeData=exPar.loadNodeData(filenames.get("Male")[nodeIndex],filenames.get("Female")[nodeIndex],dataType=float)

# Aggregate the whole landscape
exPar.sumNodesData(filenames,male=True,female=False,dataType=float)
