import graphviz
import pydotplus
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
    dotdata = tree.export_graphviz(clf, out_file=None, feature_names=["Homing", "Deposition","H Fitness", "B Fitness"], class_names=["H", "W", "R", "B"], filled=True)
    graph = pydotplus.graph_from_dot_data(dotdata)#graphviz.Source(dotdataH)
    nodes = graph.get_node_list()
    for node in nodes:
        if node.get_name() not in ('node', 'edge'):
            values = clf.tree_.value[int(node.get_name())][0]
            ratioH = float(values[0])/sum(values)
            ratioW = float(values[1])/sum(values)
            ratioB = float(values[2])/sum(values)
            #ratioR
            if(ratioH>ratioW and ratioH>ratioB):
                if(ratioH<=.2):
                    node.set_fillcolor('white')
                elif(ratioH<=0.5):
                    node.set_fillcolor('#f1d5fa')
                elif(ratioH<=0.75):
                    node.set_fillcolor('#ff65a0')
                else:
                    node.set_fillcolor('#ff004d')
            elif (ratioW>ratioH and ratioW>ratioB):
                if(ratioW<=.2):
                    node.set_fillcolor('white')
                elif(ratioW<=0.5):
                    node.set_fillcolor('#dfdcff')
                elif(ratioW<=0.75):
                    node.set_fillcolor('#8f9cff')
                else:
                    node.set_fillcolor('#4d80ff')
            elif (ratioB>ratioW and ratioB>ratioH):
                if(ratioB<=.25):
                    node.set_fillcolor('white')
                elif(ratioB<=0.5):
                    node.set_fillcolor('#eddaff')
                elif(ratioB<=0.75):
                    node.set_fillcolor('#f07bff')
                else:
                    node.set_fillcolor('#ff00ff')
            else:
                node.set_fillcolor('white')

    graph.write_png('full.png')
    # graph = graphviz.Source(dotdata)
    # graph.render()

main()
