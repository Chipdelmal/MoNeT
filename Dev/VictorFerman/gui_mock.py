import glob
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib.backends.qt_compat import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
matplotlib.use('QT5Agg')
#from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore import pyqtProperty
from mpl_toolkits.basemap import Basemap

colors = ['#ff004d','#4d80ff', '#ff00ff', 'red', 'blue', 'green', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']
def draw_pie(ax,ratios, X=0, Y=0, radius=300):
    N = len(ratios)
    xy = []
    start = 0.
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        xy1 = list(zip(x,y))
        xy.append(xy1)
        start += ratio

    for i, xyi in enumerate(xy):
        ax.scatter([X],[Y] , marker=(xyi,0), s=radius, facecolor=colors[i])

def getCoordinates(fileLocation):
    patchFile = open(fileLocation,"r")
    patchesX = []
    patchesY = []
    for line in patchFile:
        coordinates = line.split(',')
        patchesX.append(float(coordinates[0]))
        patchesY.append(float(coordinates[1]))
    patchFile.close()
    return(patchesX,patchesY)

def getSizes(fileLocation):
    populationFile = open(fileLocation,"r")
    radiuses = []
    for line in populationFile:
        radiuses.append((math.log(float(line))**2)*0.7)
    populationFile.close()
    return radiuses

def getRatios(populations, weights):
    groupPopulation= []
    total = 1
    for i in range(len(weights)):
        population = 0
        for j in range(len(weights[i])):
            population+= (populations[j]*weights[i][j])
        total+= population
        groupPopulation.append(population)
    ratios = [float(pop)/total for pop in groupPopulation]
    return ratios



class GraphicsWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(GraphicsWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.addPage(Page3(self))
        self.setWindowTitle('Visualization Wizard')

class Page1(QtWidgets.QWizardPage):
    def __init__(self,parent=None):
        super(Page1,self).__init__(parent)
        integerValidator = QtGui.QIntValidator(0,100, self)

        coordLabel = QtWidgets.QLabel('Coordinate File:')
        self.coordLine = QtWidgets.QLineEdit()
        coordBtn = QtWidgets.QPushButton('File', self)
        coordBtn.clicked.connect(self.getCoordfile)
        self.registerField('coordFile*', self.coordLine)

        popLabel = QtWidgets.QLabel('Population File:')
        self.popLine = QtWidgets.QLineEdit()
        popBtn = QtWidgets.QPushButton('File', self)
        popBtn.clicked.connect(self.getPopfile)
        self.registerField('popFile*', self.popLine)

        dataLabel = QtWidgets.QLabel('Data Directory:')
        self.dataLine = QtWidgets.QLineEdit()
        dataBtn = QtWidgets.QPushButton('File', self)
        dataBtn.clicked.connect(self.getDir)
        self.registerField('dataDir*', self.dataLine)

        allelesLabel = QtWidgets.QLabel('Number of alleles:')
        self.allelesLine = QtWidgets.QLineEdit()
        self.allelesLine.setValidator(integerValidator)
        self.registerField('alleleCount*', self.allelesLine)

        groupsLabel = QtWidgets.QLabel('Number of Groups:')
        self.groupsLine = QtWidgets.QLineEdit()
        self.groupsLine.setValidator(integerValidator)
        self.registerField('groupCount*', self.groupsLine)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(coordLabel, 1, 0)
        grid.addWidget(self.coordLine, 1, 1)
        grid.addWidget(coordBtn, 1, 2)
        grid.addWidget(popLabel, 2, 0)
        grid.addWidget(self.popLine, 2, 1)
        grid.addWidget(popBtn, 2, 2)
        grid.addWidget(dataLabel, 3, 0)
        grid.addWidget(self.dataLine, 3, 1)
        grid.addWidget(dataBtn, 3, 2)
        grid.addWidget(allelesLabel, 4, 0)
        grid.addWidget(self.allelesLine, 4, 1)
        grid.addWidget(groupsLabel, 5, 0)
        grid.addWidget(self.groupsLine, 5, 1)

        self.setLayout(grid)

    def getCoordfile(self):
        dlg = QtWidgets.QFileDialog(self, "Open File")
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fname,_ = dlg.getOpenFileName()
        self.coordLine.setText(fname)

    def getPopfile(self):
        dlg = QtWidgets.QFileDialog(self, "Open File")
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fname,_=dlg.getOpenFileName()
        self.popLine.setText(fname)

    def getDir(self):
        dlg = QtWidgets.QFileDialog(self, "Browse Directory")
        dlg.setFileMode(dlg.Directory)
        dlg.setOption(dlg.ShowDirsOnly)
        fname=str(dlg.getExistingDirectory())
        self.dataLine.setText(fname)


class Page2(QtWidgets.QWizardPage):
    def __init__(self,parent=None):
        super(Page2,self).__init__(parent)
        self.setTitle('Group-Alelle weights')
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

    def initializePage(self):
        groups = int(self.field('groupCount'))
        alleles = int(self.field('alleleCount'))
        integerValidator = QtGui.QIntValidator(0,10, self)
        vbox = self.layout()
        for i in range(groups):
            hbox = QtWidgets.QHBoxLayout()
            glabel = QtWidgets.QLabel("group "+str(i+1)+":")
            for j in range(alleles):
                label = QtWidgets.QLabel(str(j+1)+":")
                line = QtWidgets.QLineEdit()
                line.setValidator(integerValidator)
                line.setText('0')
                self.registerField(str(i)+'-'+str(j), line)
                hbox.addWidget(label)
                hbox.addWidget(line)
            vbox.addWidget(glabel)
            vbox.addLayout(hbox)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def cleanupPage(self):
        self.clearLayout(self.layout())

class Page3(QtWidgets.QWizardPage):
    def __init__(self,parent=None):
        super(Page3,self).__init__(parent)
        self.setTitle('Graph')
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        #self.toolbar = NavigationToolbar(self.canvas, self)
        #button = QtWidgets.QPushButton('Graph', self)
        #button.clicked.connect(self.plots)
        vbox = QtWidgets.QVBoxLayout()
        #vbox.addWidget(self.toolbar)
        self._timer = self.canvas.new_timer(300, [(self.plots, (), {})])
        vbox.addWidget(self.canvas)
        #vbox.addWidget(button)
        self.setLayout(vbox)
        self.patchesX = []
        self.patchesY = []
        self.minLat = 0
        self.minLong = 0
        self.maxLat = 0
        self.maxLong = 0
        self.radiuses = []
        self.columnsWeight = []
        self.files =[]
        self.lineCount = 0
        self.patches=0
        self.currentLine= 0



    def plots(self):
        if self.currentLine < self.lineCount:
            ax = self.ax
            ax.clear()
            m = Basemap(projection='merc',llcrnrlat=self.minLat-1,urcrnrlat=self.maxLat+1,llcrnrlon=self.minLong-1,urcrnrlon=self.maxLong+1,lat_ts=20,resolution='h', ax=ax)
            m.drawcoastlines(color="black")
            for patch in range(0,self.patches):
                line = next(self.files[patch]).split(',')
                sizes = [float(elem) for elem in line]
                sizes = sizes[2:]
                ratios = getRatios(sizes, self.columnsWeight)
                px,py = m(self.patchesX[patch],self.patchesY[patch])
                draw_pie(ax,ratios,px,py,self.radiuses[patch])
            self.canvas.draw()
            self.currentLine +=1
        else:
            self._timer.stop()
            for f in self.files:
                 f.close()

    def initializePage(self):
        coordFile = str(self.field('coordFile'))
        popFile = str(self.field('popFile'))
        dataFile = str(self.field('dataDir'))+"/AF1_Aggregate_Run1_*.csv"
        self.patchesX,self.patchesY = getCoordinates(coordFile)
        self.minLat = min(self.patchesY)
        self.minLong = min(self.patchesX)
        self.maxLat = max(self.patchesY)
        self.maxLong = max(self.patchesX)
        self.radiuses = getSizes(popFile)
        groups = int(self.field('groupCount'))
        alleles = int(self.field('alleleCount'))
        for i in range(groups):
            groupWeights = []
            for j in range(alleles):
                weight = int(self.field(str(i)+'-'+str(j)))
                groupWeights.append(weight)
            self.columnsWeight.append(groupWeights)
        #
        fileNames = sorted(glob.glob(dataFile))
        self.files =[]
        self.lineCount = len(open(fileNames[0]).readlines())-1
        for fileName in fileNames:
            self.files.append(open(fileName,'r'))
        self.patches=len(self.files)
        for f in self.files:
            next(f)
        self._timer.start()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = GraphicsWizard()
    wizard.show()
    sys.exit(app.exec_())
