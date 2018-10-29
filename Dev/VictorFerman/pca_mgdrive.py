import numpy as np
from sklearn.decomposition import PCA
import sys

def main():
    datasetName = sys.argv[1]
    datasetFile = open(datasetName, 'r')
    dataset=[]
    next(datasetFile)
    for line in datasetFile:
        values = line.split(',')
        homming = float(values[0])
        deposition = float(values[1])
        hFitness = float(values[2])
        bFitness = float(values[3])
        instance = [homming,deposition,hFitness,bFitness]
        dataset.append(instance)

    npDataset=np.asarray(dataset)
    pca = PCA(n_components=4)
    pca.fit(npDataset)
    print(pca.components_)
    print("\n\n ----- important -------\n\n")
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)

    datasetFile.close()

main()
