import csv

###############################################################################
# Auxiliary
###############################################################################
def readGenotypes(filename):
    reader=csv.reader(open(filename))
    return next(reader)[2:]
def generateAggregationDictionary(genotypesList,indicesList):
    aggregationDictionary={
        "genotypes": genotypesList,
        "indices": indicesList
    }
    return aggregationDictionary
