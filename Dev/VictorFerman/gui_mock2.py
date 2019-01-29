#Author vferman
#Some code was adapted from the work by Sarafina Smith and Hector Sanchez
#Creates a GUI for data anlysis, still requires further work in order to make better use of the QT capabilities

import glob
import math
import matplotlib
import numpy as np
import sys
import guiAuxFunctions as aux
import pandas as pd

from matplotlib.backends.qt_compat import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap


class GraphicsWizard(QtWidgets.QWizard):
    #MAIN class, basicaly creates a wizard in order to present the different options to the users
    def __init__(self, parent=None):
        super(GraphicsWizard, self).__init__(parent)
        self.setPage(0,StartP(self))
        self.setPage(1,Page1(self))
        self.setPage(2,Page2(self))
        self.setPage(3,Page3(self))
        self.setPage(4,Page4(self))
        self.setWindowTitle('Visualization Wizard')

class StartP(QtWidgets.QWizardPage):
    #First page of the wizard, asks for common data to all data analysis (graphing) options
    def __init__(self,parent=None):
        super(StartP,self).__init__(parent)
        integerValidator = QtGui.QIntValidator(0,10, self)

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

        self.b1 = QtWidgets.QCheckBox("Females")
        self.b1.setChecked(False)
        self.registerField('females', self.b1)

        comboLabel = QtWidgets.QLabel('Graphic Type:')
        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItem('Allele Counts')
        self.combo.addItem('Allele Heatmap')
        self.combo.addItem('Allele Stack')
        self.combo.addItem('Allele Geo-Map')
        self.registerField('graphic', self.combo)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(dataLabel, 1, 0)
        grid.addWidget(self.dataLine, 1, 1)
        grid.addWidget(dataBtn, 1, 2)
        grid.addWidget(allelesLabel, 2, 0)
        grid.addWidget(self.allelesLine, 2, 1)
        grid.addWidget(groupsLabel, 3, 0)
        grid.addWidget(self.groupsLine, 3, 1)
        grid.addWidget(self.b1, 5, 1)
        grid.addWidget(comboLabel, 4, 0)
        grid.addWidget(self.combo, 4, 1)
        self.setLayout(grid)

    def getDir(self):
        dlg = QtWidgets.QFileDialog(self, "Browse Directory")
        dlg.setFileMode(dlg.Directory)
        dlg.setOption(dlg.ShowDirsOnly)
        fname=str(dlg.getExistingDirectory())
        self.dataLine.setText(fname)

    def nextId(self):
        if self.combo.currentIndex() < 3:
            return 1
        else:
            return 3


class Page1(QtWidgets.QWizardPage):
    #Page that ask about the grouping to be done by the analysis and graphing routines. asks for group names and allele weights
    def __init__(self,parent=None):
        super(Page1,self).__init__(parent)
        self.setTitle('Group-Alelle weights')
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

    def initializePage(self):
        groups = int(self.field('groupCount'))
        alleles = int(self.field('alleleCount'))
        integerValidator = QtGui.QIntValidator(0,10, self)
        vbox = self.layout()
        for i in range(groups):
            hbox1 = QtWidgets.QHBoxLayout()
            hbox2 = QtWidgets.QHBoxLayout()
            glabel = QtWidgets.QLabel("group "+str(i+1)+":")
            gname = QtWidgets.QLineEdit()
            gname.setText('Name'+str(i))
            self.registerField('group'+str(i), gname)
            hbox1.addWidget(glabel)
            hbox1.addWidget(gname)
            for j in range(alleles):
                label = QtWidgets.QLabel(str(j+1)+":")
                line = QtWidgets.QLineEdit()
                line.setValidator(integerValidator)
                line.setText('0')
                self.registerField(str(i)+'-'+str(j), line)
                hbox2.addWidget(label)
                hbox2.addWidget(line)
            vbox.addLayout(hbox1)
            vbox.addLayout(hbox2)

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

    def nextId(self):
        if self.field('graphic') < 3:
            return 2
        else:
            return 4

class Page2(QtWidgets.QWizardPage):
    #page that presents static graphics depending on what the user chose to be presented (counts, heatmaps, stacks)
    def __init__(self,parent=None):
        super(Page2,self).__init__(parent)
        self.setTitle('Graph')
        self.figure = Figure(figsize=(20,5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = None
        self.setFinalPage(True)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)
        self.columnsWeight = []
        self.groupNames = []


    def initializePage(self):
        #wheter the user chose to do the analysis on male or female mosquitos
        if self.field('females'):
            modifier='/AF1*.csv'
        else:
            modifier='/ADM*.csv'

        #analysis setup, retrieves filenames and group related information
        dataFile = str(self.field('dataDir'))+modifier
        groups = int(self.field('groupCount'))
        alleles = int(self.field('alleleCount'))
        for i in range(groups):
            groupWeights = []
            for j in range(alleles):
                weight = int(self.field(str(i)+'-'+str(j)))
                groupWeights.append(weight)
            self.columnsWeight.append(groupWeights)
            gname = self.field('group'+str(i))
            self.groupNames.append(gname)
        fileNames = sorted(glob.glob(dataFile))

        #performs the grouping of the data in order to be graphed
        counts = aux.allCounts(fileNames, self.columnsWeight, self.groupNames)

        #graphs the data depending on what the user chose at the begining
        graphic = self.field('graphic')
        if  graphic == 0:
            #allele counts graph
            self.ax = self.figure.add_subplot(111)
            for i in range(len(counts)):
                counts[i].plot(ax=self.ax, linewidth = 0.3, legend=False, color = aux.colors[i], alpha = 0.1)
            #self.canvas.ylabel("Allele Count")
        elif graphic == 1:
            #Alelle heatmaps
            #we require one graphic for each of the groups and one for the aggregate thus we stack groups+1 graphics
            all = self.figure.add_subplot(groups+1,1,groups+1)
            for i in range(groups):
                ax = self.figure.add_subplot(groups+1,1,i+1)
                ax.imshow(counts[i].T, cmap=aux.cmaps[i])
                ax.set_yticklabels([])
                ax.set_xticklabels([])
                all.imshow(counts[i].T, cmap=aux.cmaps[i])
                time=counts[i].shape[0]
                if(time<5000):
                    ax.set_aspect(6.0)
                    all.set_aspect(6.0)
                elif (time<=10000):
                    ax.set_aspect(12.0)
                    all.set_aspect(12.0)
                else:
                    ax.set_aspect(16.0)
                    all.set_aspect(16.0)

        else:
            #alle stack graphic
            self.ax = self.figure.add_subplot(111)
            allele_dict = {}
            for i in range(groups):
                allele_dict[self.groupNames[i]] = counts[i].T.sum()
            res = pd.DataFrame(allele_dict)
            res.plot(kind = 'area', ax =self.ax, color=aux.rgba_colors)
            self.ax.set_aspect(0.0001)
        self.canvas.draw()

    def nextId(self):
        return -1

class Page3(QtWidgets.QWizardPage):
    #page required to ask for extra data regarding the map to be used and the populations on said map
    def __init__(self,parent=None):
        super(Page3,self).__init__(parent)
        integerValidator = QtGui.QIntValidator(0,10, self)

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

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(coordLabel, 1, 0)
        grid.addWidget(self.coordLine, 1, 1)
        grid.addWidget(coordBtn, 1, 2)
        grid.addWidget(popLabel, 2, 0)
        grid.addWidget(self.popLine, 2, 1)
        grid.addWidget(popBtn, 2, 2)
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

    def nextId(self):
        return 1

class Page4(QtWidgets.QWizardPage):
    #page for the presentation of the dynamic map/graph
    def __init__(self,parent=None):
        super(Page4,self).__init__(parent)
        self.setTitle('Graph')
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.setFinalPage(True)
        vbox = QtWidgets.QVBoxLayout()
        self._timer = self.canvas.new_timer(35, [(self.plots, (), {})])
        vbox.addWidget(self.canvas)
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
        #timed callback that graphs the evolution of the allele counts, stops when we reach to the last line of the experiment (last allele count)
        if self.currentLine < self.lineCount:
            ax = self.ax
            ax.clear()
            #generates the map
            m = Basemap(projection='merc',llcrnrlat=self.minLat-1,urcrnrlat=self.maxLat+1,llcrnrlon=self.minLong-1,urcrnrlon=self.maxLong+1,lat_ts=20,resolution='l', ax=ax)
            m.drawcoastlines(color="black")
            #reads each of the files and creates a pie char for each one
            for patch in range(0,self.patches):
                line = next(self.files[patch]).split(',')
                sizes = [float(elem) for elem in line]
                sizes = sizes[2:]
                ratios = aux.getRatios(sizes, self.columnsWeight)
                px,py = m(self.patchesX[patch],self.patchesY[patch])
                aux.draw_pie(ax,ratios,px,py,self.radiuses[patch])
            self.canvas.draw()
            self.currentLine +=1
        else:
            #cleanup stops the callback and closes all of the files
            self._timer.stop()
            for f in self.files:
                 f.close()

    def initializePage(self):
        #setup of the information required for the graphs
        coordFile = str(self.field('coordFile'))
        popFile = str(self.field('popFile'))
        dataFile = str(self.field('dataDir'))+"/AF1_Aggregate_Run1_*.csv"
        self.patchesX,self.patchesY = aux.getCoordinates(coordFile)
        self.minLat = min(self.patchesY)
        self.minLong = min(self.patchesX)
        self.maxLat = max(self.patchesY)
        self.maxLong = max(self.patchesX)
        self.radiuses = aux.getSizes(popFile)
        groups = int(self.field('groupCount'))
        alleles = int(self.field('alleleCount'))
        for i in range(groups):
            groupWeights = []
            for j in range(alleles):
                weight = int(self.field(str(i)+'-'+str(j)))
                groupWeights.append(weight)
            self.columnsWeight.append(groupWeights)
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
