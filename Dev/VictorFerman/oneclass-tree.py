import graphviz
import pydotplus
from sklearn import tree
import sys

def main():
    datasetName = sys.argv[1]
    datasetFile = open(datasetName, 'r')
    dataset=[]
    datasetHClass = []
    datasetWClass = []
    datasetRClass = []
    datasetBClass = []
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
            datasetHClass.append('H')
            datasetWClass.append('Other')
            datasetRClass.append('Other')
            datasetBClass.append('Other')
        elif(float(values[5])>=0.75):
            datasetHClass.append('Other')
            datasetWClass.append('W')
            datasetRClass.append('Other')
            datasetBClass.append('Other')
        elif(float(values[6])>=0.75):
            datasetHClass.append('Other')
            datasetWClass.append('Other')
            datasetRClass.append('R')
            datasetBClass.append('Other')
        else:
            datasetHClass.append('Other')
            datasetWClass.append('Other')
            datasetRClass.append('Other')
            datasetBClass.append('B')
    datasetFile.close()

    clfH = tree.DecisionTreeClassifier(max_depth=5)
    clfH.fit(dataset,datasetHClass)
    dotdataH = tree.export_graphviz(clfH, out_file=None, feature_names=["Homing", "Deposition","H Fitness", "B Fitness"], class_names=["H", "Other"], filled=True)
    graphH = pydotplus.graph_from_dot_data(dotdataH)#graphviz.Source(dotdataH)
    nodesH = graphH.get_node_list()
    for node in nodesH:
        if node.get_name() not in ('node', 'edge'):
            values = clfH.tree_.value[int(node.get_name())][0]
            ratio = float(values[0])/sum(values)
            if(ratio<=.25):
                node.set_fillcolor('white')
            elif(ratio<+0.5):
                node.set_fillcolor('#f1d5fa')
            elif(ratio<=0.75):
                node.set_fillcolor('#ff65a0')
            else:
                node.set_fillcolor('#ff004d')

    graphH.write_png('H.png')
    #graph.render('H')

    clfW = tree.DecisionTreeClassifier(max_depth=9)
    clfW.fit(dataset,datasetWClass)
    dotdataW = tree.export_graphviz(clfW, out_file=None, feature_names=["Homing", "Deposition","H Fitness", "B Fitness"], class_names=["W", "Other"], filled=True)
    graphW = pydotplus.graph_from_dot_data(dotdataW)#graphviz.Source(dotdataH)
    nodesW = graphW.get_node_list()
    for node in nodesW:
        if node.get_name() not in ('node', 'edge'):
            values = clfW.tree_.value[int(node.get_name())][0]
            ratio = float(values[0])/sum(values)
            if(ratio<=.25):
                node.set_fillcolor('white')
            elif(ratio<+0.5):
                node.set_fillcolor('#dfdcff')
            elif(ratio<=0.75):
                node.set_fillcolor('#8f9cff')
            else:
                node.set_fillcolor('#4d80ff')

    graphW.write_png('W.png')

    clfR = tree.DecisionTreeClassifier(max_depth=5)
    clfR.fit(dataset,datasetRClass)
    dotdataR= tree.export_graphviz(clfR, out_file=None, feature_names=["Homing", "Deposition","H Fitness", "B Fitness"], class_names=["R", "Other"], filled=True)
    graphR = pydotplus.graph_from_dot_data(dotdataR)#graphviz.Source(dotdataH)
    nodesR = graphR.get_node_list()
    for node in nodesR:
        if node.get_name() not in ('node', 'edge'):
            values = clfR.tree_.value[int(node.get_name())][0]
            ratio = float(values[0])/sum(values)
            if(ratio<=.25):
                node.set_fillcolor('white')
            elif(ratio<+0.5):
                node.set_fillcolor('#dacdff')
            elif(ratio<=0.75):
                node.set_fillcolor('#9b62ff')
            else:
                node.set_fillcolor('#8000ff')

    graphR.write_png('R.png')

    clfB = tree.DecisionTreeClassifier(max_depth=5)
    clfB.fit(dataset,datasetBClass)
    dotdataB = tree.export_graphviz(clfB, out_file=None, feature_names=["Homing", "Deposition","H Fitness", "B Fitness"], class_names=["B", "Other"], filled=True)
    graphB = pydotplus.graph_from_dot_data(dotdataB)#graphviz.Source(dotdataH)
    nodesB = graphB.get_node_list()
    for node in nodesB:
        if node.get_name() not in ('node', 'edge'):
            values = clfB.tree_.value[int(node.get_name())][0]
            ratio = float(values[0])/sum(values)
            if(ratio<=.25):
                node.set_fillcolor('white')
            elif(ratio<+0.5):
                node.set_fillcolor('#eddaff')
            elif(ratio<=0.75):
                node.set_fillcolor('#f07bff')
            else:
                node.set_fillcolor('#ff00ff')

    graphB.write_png('B.png')


main()
