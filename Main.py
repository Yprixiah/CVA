# Imports
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import sys
import pandas as pd
from tkinter import filedialog
import tkinter as tk
from MplWidget import MplWidget
import pickle
import numpy as np
import csv
import os

# Variables declaration
d = pd.DataFrame()
corrData = pd.DataFrame({"E/V": [], "Di/mA": []})
corrD = []
dic = {}
I = []
P = []
D = []
corrD = []
avg = []

# Window and UI construction
class Window(QDialog):

    def __init__(self):
        super().__init__()

        self.title = "Cyclic Voltammetry Analysis"
        self.left = 0
        self.top = 0
        self.width = 1024
        self.height = 768

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.InitUI()
        self.showMaximized()

    def InitUI(self):
        # Main layout
        mainBox = QVBoxLayout()
        self.setLayout(mainBox)

        # Options that apply accross the layout
        titleFont = QtGui.QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(16)

        # Hi-level layouts
        hbox1 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        hbox2 = QHBoxLayout()

        # Top-Left Panel
        buttonLoad = QPushButton('Load Data')
        buttonLoad.clicked.connect(self.load_data)
        self.fileNameLabel = QLabel()
        vbox1.addWidget(buttonLoad)
        vbox1.addWidget(self.fileNameLabel)
        vbox1.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding))

        # Top-Right Panel - Graph that plots the raw data
        buttonPlot = QPushButton('Plot raw data')
        buttonPlot.clicked.connect(self.plot_rawData)
        self.rawDataGraph = MplWidget()
        self.rawGraphToolbar = NavigationToolbar(self.rawDataGraph.canvas, self)
        vbox2 = QVBoxLayout()
        rawDataTitle = QLabel("Raw CV data")
        rawDataTitle.setFont(titleFont)
        rawDataTitle.setAlignment(Qt.AlignCenter)
        vbox2.addWidget(rawDataTitle)
        rawDataGraphHBox = QHBoxLayout()
        rawDataGraphHBox.addWidget(buttonPlot)
        rawDataGraphHBox.addWidget(self.rawGraphToolbar)
        vbox2.addLayout(rawDataGraphHBox)
        vbox2.addWidget(self.rawDataGraph)

        # Bottom-Left Panel - Graph that plots the Current vs Cycle processed data
        self.cvcLoadButton = QPushButton("Load Current Vs Cycle Data")
        self.cvcLoadButton.clicked.connect(self.loadCvcData)
        self.voltageAtSignalLabel = QLabel("Voltage at signal:  ")
        self.voltageAtSignal = QLineEdit()
        self.voltageAtSignal.setPlaceholderText("Enter voltage value at which signal is")
        self.baselineCyclesLabel = QLabel("Number of baseline cycles:   ")
        self.baselineCycles = QLineEdit()
        self.baselineCycles.setPlaceholderText("Enter the number of baseline cycles")
        self.cvcPBar = QProgressBar()
        cvcInputsVBox = QVBoxLayout()
        cvcInputsVBox.addWidget(self.cvcLoadButton)
        cvcInputsVBox.addWidget(self.voltageAtSignalLabel)
        cvcInputsVBox.addWidget(self.voltageAtSignal)
        cvcInputsVBox.addWidget(self.baselineCyclesLabel)
        cvcInputsVBox.addWidget(self.baselineCycles)
        cvcProcessButton = QPushButton('Process Data')
        cvcProcessButton.clicked.connect(self.processCvsC)
        cvcSaveButton = QPushButton("Save")
        cvcSaveButton.clicked.connect(self.saveCvcData)
        cvcPlotButton = QPushButton("Base Corr.")
        cvcPlotButton.clicked.connect(self.corrCvc)
        cvcAverageButton = QPushButton("Average")
        cvcAverageButton.clicked.connect(self.averageCVC)
        cvcButtonsVBox = QHBoxLayout()
        cvcButtonsVBox.addWidget(cvcProcessButton)
        cvcButtonsVBox.addWidget(cvcPlotButton)
        cvcButtonsVBox.addWidget(cvcSaveButton)

        cvcVBox = QVBoxLayout()
        cvcVBox.addLayout(cvcInputsVBox)
        cvcVBox.addSpacerItem(QSpacerItem(10, 30, QSizePolicy.Preferred))
        cvcVBox.addLayout(cvcButtonsVBox)
        cvcVBox.addWidget(cvcAverageButton)
        cvcVBox.addWidget(self.cvcPBar)
        cvcVBox.addSpacerItem(QSpacerItem(15, 200))

        self.cvcGraph = MplWidget()
        self.cvcToolbar = NavigationToolbar(self.cvcGraph.canvas, self)
        graphVbox = QVBoxLayout()
        graphVbox.addWidget(self.cvcToolbar)
        graphVbox.addWidget(self.cvcGraph)

        cvcHBox = QHBoxLayout()
        cvcHBox.addLayout(cvcInputsVBox)
        cvcHBox.addLayout(cvcVBox)
        cvcHBox.addLayout(graphVbox)

        currentVsCyclesTitle = QLabel('Current vs Cycles')
        currentVsCyclesTitle.setFont(titleFont)
        currentVsCyclesTitle.setAlignment(Qt.AlignCenter)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(currentVsCyclesTitle)
        vbox3.addLayout(cvcHBox)


        # Bottom-Right Panel - Graph that plots the peaks
        self.loadPeDataButton = QPushButton("Load Peak Extractor data file")
        self.loadPeDataButton.clicked.connect(self.loadPeData)
        baselineCycleLabel = QLabel('Select baseline cycle')
        dataCycleLabel = QLabel("Select data cycle")
        self.baselineComboBox = QComboBox()
        self.dataComboBox = QComboBox()
        self.peProcessButton = QPushButton('Process Data')
        self.peProcessButton.clicked.connect(self.peakExtract)
        self.peSaveButton = QPushButton("Save")
        self.peSaveButton.clicked.connect(self.savePeData)
        peButtonHBox = QHBoxLayout()
        peButtonHBox.addWidget(self.peProcessButton)
        peButtonHBox.addWidget(self.peSaveButton)
        self.pePBar = QProgressBar()
        peInputsVBox = QVBoxLayout()
        peInputsVBox.addWidget(self.loadPeDataButton)
        peInputsVBox.addWidget(baselineCycleLabel)
        peInputsVBox.addWidget(self.baselineComboBox)
        peInputsVBox.addWidget(dataCycleLabel)
        peInputsVBox.addWidget(self.dataComboBox)
        peInputsVBox.addSpacerItem(QSpacerItem(10, 30, QSizePolicy.Expanding))
        peInputsVBox.addLayout(peButtonHBox)
        peInputsVBox.addWidget(self.pePBar)
        peInputsVBox.addSpacerItem(QSpacerItem(15, 200))

        self.peGraph = MplWidget()
        self.peGraphToolbar = NavigationToolbar(self.peGraph.canvas, self)
        self.pePlotDiButton = QPushButton("Plot \u0394i")
        self.pePlotDiButton.clicked.connect(self.plotPeakExtract)
        self.pePlotall3Button = QPushButton("Plot all three curves")
        self.pePlotall3Button.clicked.connect(self.pePlotAll3)
        pePlotButtonsHBox = QHBoxLayout()
        pePlotButtonsHBox.addWidget(self.pePlotDiButton)
        pePlotButtonsHBox.addWidget(self.pePlotall3Button)
        self.savePeDataButton = QPushButton("Save \u0394i plot")
        self.savePeDataButton.clicked.connect(self.savePePlot)
        peTitleHBox = QHBoxLayout()
        pePlotVBox = QVBoxLayout()
        pePlotVBox.addLayout(pePlotButtonsHBox)
        pePlotVBox.addWidget(self.savePeDataButton)
        peTitleHBox.addLayout(pePlotVBox)
        peTitleHBox.addWidget(self.peGraphToolbar)
        vbox4 = QVBoxLayout()
        vbox4.addLayout(peTitleHBox)
        vbox4.addWidget(self.peGraph)

        peHBox = QHBoxLayout()
        peHBox.addLayout(peInputsVBox)
        peHBox.addLayout(vbox4)

        peVBox = QVBoxLayout()
        peTitleLabel = QLabel("Peak extractor")
        peTitleLabel.setFont(titleFont)
        peTitleLabel.setAlignment((Qt.AlignCenter))
        peVBox.addWidget(peTitleLabel)
        peVBox.addLayout(peHBox)

        # Layouts relationships
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(peVBox)
        mainBox.addLayout(hbox1)
        mainBox.addLayout(hbox2)

    def load_data(self):
        global d
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        d = (pd.read_csv(file_path, sep='\t', header=None))
        self.fileNameLabel.setText(file_path)
        print('Data loaded')

    def plot_rawData(self):
        self.rawDataGraph.canvas.axes.clear()
        self.rawDataGraph.canvas.axes.plot(d[0], d[1])
        # self.rawDataGraph.canvas.axes.set_title('CV data')
        self.rawDataGraph.canvas.axes.set_xlabel("E / V vs Pt")
        self.rawDataGraph.canvas.axes.set_ylabel("i / mA")
        self.rawDataGraph.canvas.draw()

    def loadCvcData(self):
        root = tk.Tk()
        root.withdraw()
        cvcFile = open(filedialog.askopenfilename(), 'rb')

    def processCvsC(self):
        # Declare local variables
        t = 0
        V = float(self.voltageAtSignal.text())
        T = []
        global D
        D = []
        print("Data processing...")
        self.cvcPBar.reset()
        self.cvcPBar.setFormat("Extracting current points...")

        # Extract the current value @ V and put it in D
        for i in range(0, (len(d) - 1)):
            j = i + 1
            k = i + 2
            A = d[i:j];
            xA = float(A[0]);
            yA = float(A[1])
            B = d[j:k];
            xB = float(B[0]);
            yB = float(B[1])
            if V > xA and V < xB:
                a = (yB - yA) / (xB - xA)
                b = yA - a * xA
                Y = a * V + b
                D.append(Y)
                t = t + 28
                T.append(t)
                self.cvcGraph.canvas.axes.clear()
                self.cvcGraph.canvas.axes.plot(D)
                self.cvcGraph.canvas.axes.set_title('Current vs Cycles @ %s' % V)
                self.cvcGraph.canvas.axes.set_xlabel("Cycle #")
                self.cvcGraph.canvas.axes.set_ylabel("\u0394i / mA")
                self.cvcGraph.canvas.draw()
            self.cvcPBar.setValue((i * 100) / len(d))
        self.cvcPBar.setValue(100)
        self.cvcPBar.setFormat("Done")

    def corrCvc(self):
        global D
        global corrD
        V = float(self.voltageAtSignal.text())
        s = int(self.baselineCycles.text())

        # Correct from baseline using the cycle number where methane starts
        if s != 0:
            m = []
            for k in range(0, s):
                m.append(D[k])
            base = sum(m) / s
            corrD = [x - base for x in D]
        elif s == 0:
            corrD = D

        self.cvcGraph.canvas.axes.clear()
        self.cvcGraph.canvas.axes.plot(corrD)
        self.cvcGraph.canvas.axes.set_title('Current vs Cycles @ %s' % V)
        self.cvcGraph.canvas.axes.set_xlabel("Cycle #")
        self.cvcGraph.canvas.axes.set_ylabel("\u0394i / mA")
        self.cvcGraph.canvas.draw()

    def saveCvcData(self):
        #cvcFileOut = asksaveasfile(mode='w')
        global corrD
        global avg
        i = 1
        with open(asksaveasfilename(), 'w') as f:
            for item in corrD:
                f.write('%s\t%s\n' %(i, item))
                i = i + 1
        f.close()

    def averageCVC(self):
        global corrD
        x = []
        e = []
        l = []
        i = 0
        global avg
        V = float(self.voltageAtSignal.text())
        s = int(self.baselineCycles.text())
        self.cvcPBar.reset()
        self.cvcPBar.setFormat("Averaging...")
        for k in range(0, len(corrD)):
            l.append(corrD[k])
            i = i + 1
            if i%s == 0 and i != 0:
                x.append(i)
                m = sum(l)/s
                avg.append(m)
                std = np.std(l)
                e.append(std)
                l = []
            self.cvcGraph.canvas.axes.clear()
            #self.cvcGraph.canvas.axes.plot(avg)
            self.cvcGraph.canvas.axes.errorbar(x, avg, e, linestyle='None', marker='o')
            self.cvcGraph.canvas.axes.set_title('Average Current vs concentration @ %s' % V)
            self.cvcGraph.canvas.axes.set_xlabel("Concentration (%)")
            self.cvcGraph.canvas.axes.set_ylabel("\u0394i / mA")
            self.cvcGraph.canvas.draw()
            self.cvcPBar.setValue((k * 100) / len(corrD))
        self.cvcPBar.setValue(100)
        self.cvcPBar.setFormat("Done")

    def peakExtract(self):
        I = []
        # dic = {}
        branch = pd.DataFrame({"E/V": [], "i/mA": []})
        x = 1
        y = 1
        self.pePBar.reset()

        # Extract E1 and E2 events from the CV file
        self.pePBar.setFormat("Extracting E1 and E2...")
        for i in range(1, (len(d) - 1)):
            h = i - 1
            j = i + 1
            if d[0][h] > d[0][j] and d[0][j] > d[0][i] or d[0][j] > d[0][h] and d[0][h] > d[0][i] or d[0][i] > d[0][
                j] and d[0][j] > d[0][h] or d[0][i] > d[0][h] and d[0][h] > d[0][j]:
                I.append(i)
                self.pePBar.setValue((i * 100) / len(d))
        self.pePBar.setValue(100)

        # Populate dic{} with anodic and cathodic branches
        self.pePBar.reset()
        self.pePBar.setFormat("Extracting Branches...")
        for i in range(0, len(d)):
            l = pd.DataFrame({"E/V": [d[0][i]], "i/mA": [d[1][i]]})
            if i in I:
                if x % 2 != 0:
                    globals()["anodic %s" % y] = str()
                    dic.update({"anodic %s" % y: branch})
                    self.baselineComboBox.addItem("anodic %s" % y)
                    self.dataComboBox.addItem("anodic %s" % y)
                    branch = pd.DataFrame({"E/V": [], "i/mA": []})
                    x = x + 1
                elif x % 2 == 0:
                    globals()["cathodic %s" % y] = str()
                    dic.update({"cathodic %s" % y: branch})
                    self.baselineComboBox.addItem("cathodic %s" % y)
                    self.dataComboBox.addItem("cathodic %s" % y)
                    branch = pd.DataFrame({"E/V": [], "i/mA": []})
                    y = y + 1
                    x = x + 1
            branch = branch.append(l, ignore_index=True)
            self.pePBar.setValue((i * 100) / len(d))
        self.pePBar.setValue(100)
        self.pePBar.setFormat("Done.")

    def plotPeakExtract(self):
        global corrData
        self.pePBar.reset()
        self.peGraph.canvas.axes.clear()

        #Subtract baseline current from data current
        corrData.drop(columns = ["E/V", "Di/mA"])
        corrData = pd.DataFrame({"E/V": [], "Di/mA": []})
        self.pePBar.setFormat("Plotting...")
        for i in range(0, len(dic[self.baselineComboBox.currentText()])):
            v = dic[self.dataComboBox.currentText()]['i/mA'][i] - dic[self.baselineComboBox.currentText()]['i/mA'][i]
            m = pd.DataFrame({"E/V": [dic[self.baselineComboBox.currentText()]['E/V'][i]], "Di/mA": [v]})
            corrData = corrData.append(m, ignore_index=True)
            self.pePBar.setValue((i * 100) / len(dic[self.baselineComboBox.currentText()]))
        self.pePBar.setValue(100)
        self.pePBar.setFormat("Done")

        #Plotting
        self.peGraph.canvas.axes.clear()
        self.peGraph.canvas.axes.plot(corrData['E/V'], corrData['Di/mA'])
        self.peGraph.canvas.axes.set_title("Corrected %s" % self.dataComboBox.currentText())
        self.peGraph.canvas.axes.set_xlabel("E / V vs Pt")
        self.peGraph.canvas.axes.set_ylabel("\u0394i / mA")

    def pePlotAll3(self):
        global corrData
        self.pePBar.reset()
        self.pePBar.setFormat("Plotting...")
        self.peGraph.canvas.axes.clear()

        # Subtract baseline current from data current
        corrData.drop(columns=["E/V", "Di/mA"])
        corrData = pd.DataFrame({"E/V": [], "Di/mA": []})
        for i in range(0, len(dic[self.baselineComboBox.currentText()])):
            v = dic[self.dataComboBox.currentText()]['i/mA'][i] - dic[self.baselineComboBox.currentText()]['i/mA'][i]
            m = pd.DataFrame({"E/V": [dic[self.baselineComboBox.currentText()]['E/V'][i]], "Di/mA": [v]})
            corrData = corrData.append(m, ignore_index=True)
            self.pePBar.setValue((i * 100) / len(dic[self.baselineComboBox.currentText()]))
        self.pePBar.setFormat("Done")
        self.pePBar.setValue(100)

        # Plotting
        self.peGraph.canvas.axes.plot(dic[self.baselineComboBox.currentText()]['E/V'], dic[self.baselineComboBox.currentText()]['i/mA'], label="Baseline cycle", color="black")
        self.peGraph.canvas.axes.plot(dic[self.dataComboBox.currentText()]['E/V'], dic[self.dataComboBox.currentText()]['i/mA'], label="Data cycle", color="grey")
        self.peGraph.canvas.axes.plot(corrData['E/V'], corrData['Di/mA'], label="\u0394i", color="red")
        self.peGraph.canvas.axes.set_xlabel("E / V vs Pt")
        self.peGraph.canvas.axes.set_ylabel("mA")

    def loadPeData(self):
        global dic
        root = tk.Tk()
        root.withdraw()
        peFileIn = open(filedialog.askopenfilename(), 'rb')
        dic = pickle.load(peFileIn)
        k = 1
        self.pePBar.reset()
        for key in dic.keys():
            k = k + 1
            self.baselineComboBox.addItem(key)
            self.dataComboBox.addItem(key)
            self.pePBar.setValue((k*100)/len(dic.keys()))
        self.pePBar.setValue(100)
        self.pePBar.setFormat("Data loaded")

    def savePeData(self):
        peFileOut = asksaveasfile(mode='wb')
        pickle.dump(dic, peFileOut)
        peFileOut.close()

    def savePePlot(self):
        global corrData
        peFileOut = asksaveasfile(mode='w')
        corrData.to_csv(peFileOut, index=False, sep='\t')
        peFileOut.close()

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
