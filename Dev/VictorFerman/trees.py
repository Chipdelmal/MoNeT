import graphviz
from sklearn import tree
import sys

def main():
    datasetName = sys.argv[1]
    datasetFile = open(datasetName, 'r')
    dataset=[]
    datasetClasses = []
    next(datasetFile)
    for line in datasetFile:
        values = line.split(',')
        homming = float(values[0])
        deposition = float(values[1])
        hFitness = float(values[2])
        bFitness = float(values[3])
        instance = [homming,deposition,hFitness,bFitness]
        dataset.append(instance)
        if(float(values[4])>=0.75):
            datasetClasses.append('H')
        elif(float(values[5])>=0.75):
            datasetClasses.append('W')
        elif(float(values[6])>=0.75):
            datasetClasses.append('R')
        else:
            datasetClasses.append('B')
    datasetFile.close()

    clf = tree.DecisionTreeClassifier()
    clf.fit(dataset,datasetClasses)
    dotdata = tree.export_graphviz(clf, out_file=None, feature_names=["Homming", "Deposition","H Fitness", "B Fistness"], class_names=["H", "W", "R", "B"], filled=True)
    graph = graphviz.Source(dotdata)
    graph.render()

main()
